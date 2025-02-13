# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

class KsGlobalDiscountSales(models.Model):
    _inherit = "sale.order"

    ks_global_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount Type',
                                               readonly=True,
                                               states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                                               default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount',
                                           readonly=True,
                                           states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount', readonly=True, compute='_amount_all', store=True,
                                         track_visibility='always')
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')
    amount_before_discount = fields.Monetary(string='Amount Before Discount', store=True, compute='_amount_all', tracking=4)

    @api.depends('company_id.ks_enable_discount')
    def ks_verify_discount(self):
        for rec in self:
            rec.ks_enable_discount = rec.company_id.ks_enable_discount

    # @api.depends('order_line.price_total', 'order_line.price_subtotal','ks_global_discount_rate','special_discount_type','special_discount', 'ks_global_discount_type')
    # def _amount_all(self):
    #     res = super(KsGlobalDiscountSales, self)._amount_all()
    #     for rec in self:
    #         if not ('ks_global_tax_rate' in rec):
    #             rec.ks_calculate_discount()
    #         # amount_before_discount = sum(line.quantity * line.price_unit for line in rec.order_line.filtered(lambda r: not r.is_downpayment))
    #         amount_before_discount = rec.amount_untaxed
    #         amount_total = rec.amount_untaxed - rec.ks_amount_discount -rec.special_discount + rec.amount_tax
    #         amount_untaxed = rec.amount_untaxed - rec.ks_amount_discount
    #         amount_tax = rec.amount_tax
    #         order_lines_with_taxes = rec.order_line.filtered(lambda r: r.tax_id)
    #         if rec.ks_global_discount_rate and rec.ks_global_discount_type and order_lines_with_taxes:
    #             line = order_lines_with_taxes[0]
    #             price = rec.amount_untaxed - rec.ks_amount_discount - rec.special_discount
    #             taxes = line.tax_id.compute_all(price, line.order_id.currency_id, 1, product=False, partner=line.order_id.partner_shipping_id)
    #             amount_tax =  sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
    #             amount_total = amount_untaxed + amount_tax
    #         rec.update({
    #             'amount_untaxed': amount_untaxed,
    #             'amount_tax':  amount_tax,
    #             'amount_total': amount_total,
    #             'amount_before_discount': amount_before_discount,
    #         })
            
    #     return res
    
    # @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    # def _compute_tax_totals_json(self):
    #     def compute_universal_taxes(order_line):
    #         order = order_line.order_id
    #         price = order.amount_untaxed
    #         return order_line.tax_id._origin.compute_all(price, order.currency_id,1, product=False, partner=order.partner_shipping_id)

    #     not_universal_order = self.filtered(lambda r: not r.ks_global_discount_rate or not r.ks_global_discount_type or not r.order_line.filtered(lambda s: s.tax_id))    
    #     super(KsGlobalDiscountSales,not_universal_order)._compute_tax_totals_json()
        
    #     account_move = self.env['account.move']
    #     for order in (self - not_universal_order):
    #         tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line.filtered(lambda r: r.tax_id)[0], compute_universal_taxes)
    #         tax_totals = account_move.with_context({'universal_discount': order.ks_amount_discount})._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
    #         order.tax_totals_json = json.dumps(tax_totals)

    # @api.multi
    def _prepare_invoice(self):
        res = super(KsGlobalDiscountSales, self)._prepare_invoice()
        for rec in self:
            res['ks_global_discount_rate'] = rec.ks_global_discount_rate
            res['ks_global_discount_type'] = rec.ks_global_discount_type
        return res

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
            # rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ks_amount_discount

    def get_universal_discount_rate(self):
        self.ensure_one()
        rate = 0.0
        if self.ks_global_discount_type == "amount" and self.ks_global_discount_rate:
            total_lines = sum(line.product_uom_qty * line.price_unit for line in self.order_line.filtered(lambda r: not r.is_downpayment))
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


    @api.constrains('order_line', 'order_line.tax_id', 'ks_global_discount_rate', 'ks_global_discount_type')
    def check_order_line_tax_id(self):
        """
        Constrains on order line taxes in case of universal discount
        """
        for rec in self:
            if not rec.ks_global_discount_rate or not rec.ks_global_discount_type:
                continue
            order_line_with_taxes = rec.order_line.filtered(lambda r: not r.display_type and not r.is_downpayment and r.tax_id)
            if len(rec.order_line) <= 1 or not order_line_with_taxes:
                continue
            tax_id = order_line_with_taxes[0].tax_id
            for line in rec.order_line.filtered(lambda r: not r.display_type and not r.is_downpayment):
                if line.tax_id != tax_id:
                    raise ValidationError(_('All order details should have the same taxes or all of them should have not taxes.'))
                    
class KsSaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(KsSaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if invoice and self.advance_payment_method == 'delivered':
            invoice['ks_global_discount_rate'] = order.ks_global_discount_rate
            invoice['ks_global_discount_type'] = order.ks_global_discount_type
        return invoice
    
    def _prepare_invoice_values(self, order, name, amount, so_line):
        
        invoice_vals = super(KsSaleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        if invoice_vals and invoice_vals['invoice_line_ids'] and self.advance_payment_method != 'delivered': 
            invoice_vals['invoice_line_ids'][0][2]['is_downpayment'] = True
        
        return invoice_vals

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res['is_downpayment'] = self.is_downpayment
        
        return res
    
    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id', 'order_id.ks_amount_discount')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        super(SaleOrderLine, self)._compute_amount()
        for line in self.filtered(lambda r: r.order_id.ks_amount_discount):
            _logger.info("====================_compute_amount")
            _logger.info(self)
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            rate = line.order_id.get_universal_discount_rate()
            price = price * (1 - (rate or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                # 'price_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])