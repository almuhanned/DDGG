# -*- coding: utf-8 -*-
import json
from re import S

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class KSGlobalDiscountPurchases(models.Model):
    _inherit = "purchase.order"

    ks_global_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount Type', readonly=True,
                                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                               default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount', readonly=True,
                                           states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount', readonly=True, compute='_amount_all',
                                         track_visibility='always', store=True)
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')
    amount_before_discount = fields.Monetary(string='Amount Before Discount', store=True, compute='_amount_all', tracking=4)

    @api.depends('company_id.ks_enable_discount')
    def ks_verify_discount(self):
        for rec in self:
            rec.ks_enable_discount = rec.company_id.ks_enable_discount

    @api.depends('order_line.price_total', 'ks_global_discount_type', 'ks_global_discount_rate')
    def _amount_all(self):
        ks_res = super(KSGlobalDiscountPurchases, self)._amount_all()
        for rec in self:
            if not ('global_tax_rate' in rec):
                rec.ks_calculate_discount()
            # amount_before_discount = sum(line.product_qty * line.price_unit for line in rec.order_line)
            amount_before_discount = rec.amount_untaxed
            amount_total = rec.amount_untaxed - rec.ks_amount_discount + rec.amount_tax
            amount_untaxed = rec.amount_untaxed - rec.ks_amount_discount
            amount_tax = rec.amount_tax
            order_lines_with_taxes = rec.order_line.filtered(lambda r: r.taxes_id)
            if rec.ks_amount_discount and order_lines_with_taxes:
                line = order_lines_with_taxes[0]
                price = rec.amount_untaxed - rec.ks_amount_discount
                taxes = line.taxes_id.compute_all(price, line.order_id.currency_id, 1, product=False, partner=line.order_id.partner_id)
                amount_tax =  sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                amount_total = amount_untaxed + amount_tax
            rec.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax':  amount_tax,
                'amount_total': amount_total,
                'amount_before_discount': amount_before_discount,
            })
        return ks_res
    
    @api.depends('order_line.taxes_id', 'order_line.price_subtotal', 'amount_total', 'amount_untaxed')
    def  _compute_tax_totals_json(self):
        def compute_universal_taxes(order_line):
            order = order_line.order_id
            price = order.amount_untaxed
            return order_line.taxes_id._origin.compute_all(price, order.currency_id,1, product=False, partner=order.partner_id)
        
        not_universal_order = self.filtered(lambda r: not r.ks_global_discount_rate or not r.ks_global_discount_type or not r.order_line.filtered(lambda s: s.taxes_id))    
        super(KSGlobalDiscountPurchases,not_universal_order)._compute_tax_totals_json()
        
        account_move = self.env['account.move']
        for order in (self - not_universal_order):
            
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line.filtered(lambda r: r.taxes_id)[0], compute_universal_taxes)
            tax_totals = account_move.with_context({'universal_discount': order.ks_amount_discount})._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)

    def _prepare_invoice(self):
        ks_res = super(KSGlobalDiscountPurchases, self)._prepare_invoice()
        ks_res['ks_global_discount_type'] = self.ks_global_discount_type
        ks_res['ks_global_discount_rate'] = self.ks_global_discount_rate
        ks_res['special_discount_rate'] = 0
        ks_res['special_discount_type'] = self.ks_global_discount_type
                
        return ks_res

    def action_view_invoice(self, invoices=False):
        ks_res = super(KSGlobalDiscountPurchases, self).action_view_invoice()
        for rec in self:
            hh = ks_res['context']
            jj = str(hh).replace("'", '"')
            dic = json.loads(jj)
            dic['default_ks_global_discount_rate'] = rec.ks_global_discount_rate
            dic['default_ks_global_discount_type'] = rec.ks_global_discount_type
            dic['default_special_discount_rate'] = 0
            dic['default_special_discount_type'] = self.ks_global_discount_type
            context_str = json.dumps(dic)
            ks_res['context'] = context_str
            # ks_res['context']['default_ks_global_discount_rate'] = rec.ks_global_discount_rate
            # ks_res['context']['default_ks_global_discount_type'] = rec.ks_global_discount_type
        return ks_res

    # @api.multi
    def ks_calculate_discount(self):
        for rec in self:
            if rec.ks_global_discount_type == "amount":
                rec.ks_amount_discount = rec.ks_global_discount_rate if rec.amount_untaxed > 0 else 0
            elif rec.ks_global_discount_type == "percent":
                if rec.ks_global_discount_rate != 0.0:
                    # rec.ks_amount_discount = (rec.amount_untaxed + rec.amount_tax) * rec.ks_global_discount_rate / 100
                    rec.ks_amount_discount = (rec.amount_untaxed) * rec.ks_global_discount_rate / 100
                else:
                    rec.ks_amount_discount = 0
            elif not rec.ks_global_discount_type:
                rec.ks_amount_discount = 0
                rec.ks_global_discount_rate = 0
            # rec.amount_total = rec.amount_tax + rec.amount_untaxed - rec.ks_amount_discount

    def get_universal_discount_rate(self):
        self.ensure_one()
        rate = 0.0
        if self.ks_global_discount_type == "amount" and self.ks_global_discount_rate:
            total_lines = sum(line.product_qty * line.price_unit for line in self.order_line)
            rate = (self.ks_global_discount_rate / total_lines) * 100 if total_lines > 0 else 0
        elif self.ks_global_discount_type == "percent" and self.ks_global_discount_rate:
            rate = self.ks_global_discount_rate
        return rate
    
    @api.constrains('ks_global_discount_rate')
    def ks_check_discount_value(self):
        if self.ks_global_discount_type == "percent":
            if self.ks_global_discount_rate > 100 or self.ks_global_discount_rate < 0:
                raise ValidationError('You cannot enter percentage value greater than 100.')
        else:
            if self.ks_global_discount_rate < 0 or self.ks_global_discount_rate > self.amount_untaxed:
                raise ValidationError(
                    'You cannot enter discount amount greater than actual cost or value lower than 0.')

    
    @api.constrains('order_line', 'order_line.taxes_id', 'ks_global_discount_rate', 'ks_global_discount_type')
    def check_order_line_taxes_id(self):
        """
        Constrains on order line taxes in case of universal discount
        """
        for rec in self:
            if not rec.ks_global_discount_rate or not rec.ks_global_discount_type:
                continue
            order_line_with_taxes = rec.order_line.filtered(lambda r: not r.display_type and r.taxes_id)
            if len(rec.order_line) <= 1 or not order_line_with_taxes:
                continue
            taxes_id = order_line_with_taxes[0].taxes_id
            for line in rec.order_line.filtered(lambda r: not r.display_type):
                if line.taxes_id != taxes_id:
                    raise ValidationError(_('All order details should have the same taxes or all of them should have not taxes.'))

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    @api.depends('product_qty', 'price_unit', 'taxes_id', 'order_id.ks_amount_discount')
    def _compute_amount(self):
        super(PurchaseOrderLine, self)._compute_amount()
        for line in self.filtered(lambda r: r.order_id.ks_amount_discount):
            vals = line._prepare_compute_all_values()
            price = line.price_unit
            # price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            rate = line.order_id.get_universal_discount_rate()
            price = price * (1 - (rate or 0.0) / 100.0)
            vals['price_unit'] = price
            taxes = line.taxes_id.compute_all(**vals)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                # 'price_subtotal': taxes['total_excluded'],
            })