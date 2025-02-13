# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class KsGlobalDiscountSales(models.Model):
    _inherit = "sale.order"


    special_discount_type = fields.Selection([('percent', 'Percentage'), ('amount', 'Amount')],
                                               string='Universal Discount Type',
                                               readonly=False,
                                               default='percent')

    special_discount_rate = fields.Float('Special Discount')
    
    special_discount = fields.Monetary(string='Special Discount',
                                         readonly=True,
                                         compute='_amount_all',
                                         store=True, track_visibility='always')


    
    @api.depends('order_line.price_total', 'order_line.price_subtotal','ks_global_discount_rate','special_discount_rate','special_discount_type','special_discount', 'ks_global_discount_type')
    def _amount_all(self):
        res = super(KsGlobalDiscountSales, self)._amount_all()
        for rec in self:
            if not ('ks_global_tax_rate' in rec):
                rec.ks_calculate_discount()

            # amount_before_discount = sum(line.quantity * line.price_unit for line in rec.order_line.filtered(lambda r: not r.is_downpayment))
            amount_before_discount = rec.amount_untaxed
            amount_total = rec.amount_untaxed - rec.ks_amount_discount -rec.special_discount + rec.amount_tax
            amount_untaxed = rec.amount_untaxed - rec.ks_amount_discount - rec.special_discount
            amount_tax = rec.amount_tax
            order_lines_with_taxes = rec.order_line.filtered(lambda r: r.tax_id)
            if (rec.ks_global_discount_rate and rec.ks_global_discount_type and order_lines_with_taxes) or ( rec.special_discount_rate and rec.special_discount_type and order_lines_with_taxes):
                line = order_lines_with_taxes[0]
                price = rec.amount_untaxed - rec.ks_amount_discount - rec.special_discount
                taxes = line.tax_id.compute_all(price, line.order_id.currency_id, 1, product=False, partner=line.order_id.partner_shipping_id)
                amount_tax =  sum(t.get('amount', 0.0) for t in taxes.get('taxes', []))
                amount_total = amount_untaxed + amount_tax
                # print("############################### price",price)
                # print("############################### taxes",taxes)
                # print("############################### amount_tax",amount_tax)
            rec.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax':  amount_tax,
                'amount_total': amount_total,
                'amount_before_discount': amount_before_discount,
            })
            
        return res
    # @api.depends('order_line.price_total', 'order_line.price_subtotal','ks_global_discount_rate', \
    #     'ks_global_discount_type','special_discount','special_discount_type','special_discount_rate')
    # def _amount_all(self):
    #     res = super(KsGlobalDiscountSales, self)._amount_all()
        
    #     for rec in self:
            
    #         amount_before_discount = rec.amount_untaxed
    #         amount_total = rec.amount_untaxed - rec.special_discount + rec.amount_tax
    #         amount_untaxed = rec.amount_untaxed - rec.special_discount
    #         amount_tax = rec.amount_tax
    #         order_lines_with_taxes = rec.order_line.filtered(lambda r: r.tax_id)
    #         if rec.special_discount_rate and rec.special_discount_type and order_lines_with_taxes:
    #             line = order_lines_with_taxes[0]
    #             price = rec.amount_untaxed - rec.special_discount
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



    def ks_calculate_discount(self):
        super(KsGlobalDiscountSales, self).ks_calculate_discount()
        for rec in self:
            if rec.special_discount_type == "amount":
                rec.special_discount = rec.special_discount_rate if rec.amount_untaxed > 0 else 0

            elif rec.special_discount_type == "percent":
                if rec.special_discount_rate != 0.0:
                    # rec.ks_amount_discount = (rec.amount_untaxed + rec.amount_tax) * rec.ks_global_discount_rate / 100
                    rec.special_discount = (rec.amount_untaxed - rec.ks_amount_discount) * rec.special_discount_rate / 100
                else:
                    rec.special_discount = 0
            elif not rec.special_discount_type:
                rec.special_discount = 0
                rec.special_discount_rate = 0
            # rec.amount_total = rec.amount_untaxed + rec.amount_tax - rec.ks_amount_discount


    def _prepare_invoice(self):
        res = super(KsGlobalDiscountSales, self)._prepare_invoice()
        for rec in self:
            res['special_discount_rate'] = rec.special_discount_rate
            res['special_discount_type'] = rec.special_discount_type
        return res


    @api.depends('order_line.tax_id', 'order_line.price_unit','special_discount_rate', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_universal_taxes(order_line):
            order = order_line.order_id
            price = order.amount_untaxed
            return order_line.tax_id._origin.compute_all(price, order.currency_id,1, product=False, partner=order.partner_shipping_id)
        not_universal_order = self.filtered(lambda r: not r.ks_global_discount_rate or not r.ks_global_discount_type or not r.order_line.filtered(lambda s: s.tax_id))    
        super(KsGlobalDiscountSales,self)._compute_tax_totals_json()
        account_move = self.env['account.move']
        for order in (self):
            if len(order.order_line) > 0 :
                tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line.filtered(lambda r: r.tax_id)[0], compute_universal_taxes)
                tax_totals = account_move.with_context({'universal_discount': order.ks_amount_discount})._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
                order.tax_totals_json = json.dumps(tax_totals)

class KsSaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(KsSaleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        if invoice and self.advance_payment_method == 'delivered':
            invoice['special_discount_rate'] = order.ks_global_discount_rate
            invoice['special_discount_type'] = order.ks_global_discount_type
        return invoice
    
   