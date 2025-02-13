# -*- coding: utf-8 -*-
import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang


class KsGlobalDiscountInvoice(models.Model):
    # _inherit = "account.invoice"
    """ changing the model to account.move """
    _inherit = "account.move"

    ks_global_discount_type = fields.Selection([
        ('percent', 'Percentage'),
        ('amount', 'Amount')],
        string='Universal Discount Type',
        readonly=True,
        states={'draft': [('readonly', False)],
                'sent': [('readonly', False)]},
        default='percent')
    ks_global_discount_rate = fields.Float('Universal Discount',
                                           readonly=True,
                                           states={'draft': [('readonly', False)],
                                                   'sent': [('readonly', False)]})
    ks_amount_discount = fields.Monetary(string='Universal Discount',
                                         readonly=True,
                                         compute='_compute_amount',
                                         store=True, track_visibility='always')
    ks_enable_discount = fields.Boolean(compute='ks_verify_discount')
    ks_sales_discount_account_id = fields.Integer(compute='ks_verify_discount')
    ks_purchase_discount_account_id = fields.Integer(compute='ks_verify_discount')
    amount_before_discount = fields.Monetary(string='Amount Before Discount', store=False, tracking=4)

    @api.depends('company_id.ks_enable_discount')
    def ks_verify_discount(self):
        for rec in self:
            rec.ks_enable_discount = rec.company_id.ks_enable_discount
            rec.ks_sales_discount_account_id = rec.company_id.ks_sales_discount_account.id
            rec.ks_purchase_discount_account_id = rec.company_id.ks_purchase_discount_account.id

    # # 1. tax_line_ids is replaced with tax_line_id. 2. api.multi is also removed.
    # @api.depends(
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.payment_id.is_matched',
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_debit_ids.debit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.payment_id.is_matched',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual',
    #     'line_ids.matched_credit_ids.credit_move_id.move_id.line_ids.amount_residual_currency',
    #     'line_ids.debit',
    #     'line_ids.credit',
    #     'line_ids.currency_id',
    #     'line_ids.amount_currency',
    #     'line_ids.amount_residual',
    #     'line_ids.amount_residual_currency',
    #     'line_ids.payment_id.state',
    #     'line_ids.full_reconcile_id'    ,
    #     'ks_global_discount_type',
    #     'ks_global_discount_rate')
    # def _compute_amount(self):
    #     super(KsGlobalDiscountInvoice, self)._compute_amount()
    #     for rec in self:
    #         rec.amount_before_discount = rec.amount_untaxed
    #         if not rec.ks_global_discount_rate:
    #             continue
    #         if not ('ks_global_tax_rate' in rec):
    #             rec.ks_calculate_discount()
    #         # sign = rec.move_type in ['in_refund', 'out_refund'] and -1 or 1
    #         if rec.move_type == 'entry' or rec.is_outbound():
    #             sign = 1
    #         else:
    #             sign = -1
    #         currencies = rec._get_lines_onchange_currency().currency_id
    #         universal_line = rec.line_ids.filtered(
    #                     lambda line: line.name and line.name.find('Universal Discount') == 0)
    #         # rec.amount_before_discount = sum(line.quantity * line.price_unit for line in rec.invoice_line_ids.filtered(lambda r: not r.is_downpayment))
    #         rec.amount_before_discount = rec.amount_untaxed
            
    #         if universal_line:
    #             rec.amount_untaxed = rec.amount_untaxed + sign * (universal_line.amount_currency if len(currencies) == 1 else universal_line.balance)
    #             rec.amount_total = rec.amount_total + sign * (universal_line.amount_currency if len(currencies) == 1 else universal_line.balance)
    #             rec.amount_total_signed = rec.amount_total_signed + (abs(universal_line.balance) if rec.move_type == 'entry' else - universal_line.balance)
    #             rec.amount_total_in_currency_signed = abs(rec.amount_total) if rec.move_type == 'entry' else -(sign * rec.amount_total)
            
            
            

    # @api.multi
    # def ks_calculate_discount(self):
    #     print("########################### ks_calculate_discount universal")
    #     for rec in self:
    #         if rec.ks_global_discount_type == "amount":
    #             rec.ks_amount_discount = rec.ks_global_discount_rate if rec.amount_untaxed > 0 else 0
    #         elif rec.ks_global_discount_type == "percent":
    #             if rec.ks_global_discount_rate != 0.0:
    #                 # rec.ks_amount_discount = (rec.amount_untaxed + rec.amount_tax) * rec.ks_global_discount_rate / 100
    #                 amount = sum(line.price_subtotal for line in rec.line_ids.filtered(lambda r: not r.exclude_from_invoice_tab and not r.is_downpayment))
    #                 rec.ks_amount_discount = (amount) * rec.ks_global_discount_rate / 100
    #             else:
    #                 rec.ks_amount_discount = 0
    #         elif not rec.ks_global_discount_type:
    #             rec.ks_global_discount_rate = 0
    #             rec.ks_amount_discount = 0
    #         for line in rec.invoice_line_ids:
    #             line.update(line._get_price_total_and_subtotal())
    #         # rec.amount_total = rec.amount_tax + rec.amount_untaxed - rec.ks_amount_discount
    #         # rec.ks_update_universal_discount()
        
    def get_universal_discount_rate(self):
        # self.ensure_one()
        for rec in self :
            rate = 0.0
            if rec.ks_global_discount_type == "amount" and rec.ks_global_discount_rate:
                total_lines = sum(line.quantity * line.price_unit for line in self.invoice_line_ids.filtered(lambda r: not r.is_downpayment))
                rate = (rec.ks_global_discount_rate / total_lines) * 100 if total_lines > 0 else 0
            elif rec.ks_global_discount_type == "percent" and rec.ks_global_discount_rate:
                rate = rec.ks_global_discount_rate
            return rate
                     
    # @api.onchange('ks_global_discount_rate','special_discount_rate','special_discount_type','special_discount', 'ks_global_discount_type')
    # def _onchange_ks_amount_discount(self):
    #     """
    #     """
    #     self.ks_calculate_discount()
    #     for line in self.invoice_line_ids:
    #         line.update(line._get_price_total_and_subtotal())
    #     self._recompute_dynamic_lines(recompute_all_taxes=True)

    @api.constrains('ks_global_discount_rate')
    def ks_check_discount_value(self):
        if self.ks_global_discount_type == "percent":
            if self.ks_global_discount_rate > 100 or self.ks_global_discount_rate < 0:
                raise ValidationError('You cannot enter percentage value greater than 100.')
        else:
            if self.ks_global_discount_rate < 0 or self.amount_untaxed < 0:
                raise ValidationError(
                    'You cannot enter discount amount greater than actual cost or value lower than 0.')

    @api.model
    def _prepare_refund(self, invoice, date_invoice=None, date=None, description=None, journal_id=None):
        ks_res = super(KsGlobalDiscountInvoice, self)._prepare_refund(invoice, date_invoice=None, date=None,
                                                                      description=None, journal_id=None)
        ks_res['ks_global_discount_rate'] = self.ks_global_discount_rate
        ks_res['ks_global_discount_type'] = self.ks_global_discount_type
        return ks_res


    # @api.onchange('ks_global_discount_rate', 'ks_global_discount_type', 'line_ids')
    def _recompute_universal_discount_lines(self):
        """This Function Create The General Entries for Universal Discount"""
        print("#################################### _recompute_universal_discount_lines universal")
        for rec in self:
            print("########  werewrewrewrewrewrewrewrewrewrew ##########")
            type_list = ['out_invoice', 'out_refund', 'in_invoice', 'in_refund']
            if rec.ks_amount_discount == 0:
                already_exists = rec.line_ids.filtered(
                        lambda line: line.name and line.name.find('Universal Discount') == 0)
                rec.line_ids -= already_exists
            if rec.ks_global_discount_rate > 0 and rec.move_type in type_list:
                if rec.is_invoice(include_receipts=True):
                    in_draft_mode = self != self._origin
                    ks_name = "Universal Discount "
                    if rec.ks_global_discount_type == "amount":
                        ks_value = "of amount #" + str(self.ks_global_discount_rate)
                    elif rec.ks_global_discount_type == "percent":
                        ks_value = " @" + str(self.ks_global_discount_rate) + "%"
                    else:
                        ks_value = ''
                    ks_name = ks_name + ks_value
                    
                    already_exists = rec.line_ids.filtered(
                        lambda line: line.name and line.name.find('Universal Discount') == 0)
                    
                    amount = rec.ks_amount_discount
                    amount_currency = amount
                    if rec.currency_id != rec.company_id.currency_id:
                        amount = rec.currency_id._convert(amount_currency, rec.company_id.currency_id, rec.company_id, rec.date or rec.invoice_date)
                    
                    sign = rec.move_type in ["out_invoice", "in_refund"] and 1 or -1
                    amount = sign * amount
                    amount_currency = sign * amount_currency
                    
                    if already_exists:
                        if rec.move_type in ["out_invoice", "in_refund"]:
                            debit = abs(amount) 
                            credit = 0.0
                        else:
                            debit =  0.0
                            credit = abs(amount) 
                        print("########  werewrewrewrewrewrewrewrewrewrew  22222222222222222 ##########")
                        print("###################   wrewrewr amount",amount)
                        print("###################   ewrewrew  credit",credit)
                        print("##################### ewrewrrewr debit",debit)
                        print("##################### ewrewrrewr debit",self.env.context)
                        if rec.ks_sales_discount_account_id \
                                and (rec.move_type in ["out_invoice", "out_refund"]):
                            
                            already_exists.update({
                                'name': ks_name,
                                'debit': amount > 0.0 and amount or 0.0,
                                'credit': amount < 0.0 and -amount or 0.0,
                                'amount_currency': amount_currency,
                                'currency_id': rec.currency_id.id,
                            })
                            
                        if rec.ks_purchase_discount_account_id \
                                and (rec.move_type in ["in_invoice", "in_refund"]):
                            
                            already_exists.update({
                                'name': ks_name,
                                'debit': amount < 0.0 and -amount or 0.0,
                                'credit': amount > 0.0 and amount or 0.0,
                                'amount_currency': amount_currency,
                                'currency_id': rec.currency_id.id,
                            })
                            
                    else:
                        new_tax_line = self.env['account.move.line']
                        create_method = in_draft_mode and \
                                        self.env['account.move.line'].new or \
                                        self.env['account.move.line'].create
                        account_id = rec.move_type in ["out_invoice", "out_refund"] and rec.ks_sales_discount_account_id or rec.ks_purchase_discount_account_id
                        if rec.move_type in ["out_invoice", "in_refund"]:
                            debit = abs(amount) 
                            credit = 0.0
                        else:
                            debit =  0.0
                            credit = abs(amount) 
                    
                        dict = {
                            'move_name': self.name,
                            'name': ks_name,
                            # 'price_unit': self.ks_amount_discount,
                            'quantity': 1,
                            'debit': debit,
                            'credit': credit,
                            'amount_currency': amount_currency,
                            'currency_id': rec.currency_id.id,
                            'account_id': account_id,
                            # 'move_id': self._origin,
                            'move_id': rec.id,
                            'date': rec.date,
                            'exclude_from_invoice_tab': True,
                            'partner_id': rec.partner_id and rec.partner_id.id or False,
                            'company_id': rec.company_id.id,
                            'company_currency_id': rec.company_currency_id.id,
                        }
                        print("#################################### dict universal",dict)
                        candidate = create_method(dict)
                        
                        
    # @api.constrains('invoice_line_ids', 'invoice_line_ids.tax_ids', 'ks_global_discount_rate', 'ks_global_discount_type','special_discount_rate','special_discount_type','special_discount',)
    # def check_invoice_line_ids_tax_ids(self):
    #     """
    #     Constrains on order line taxes in case of universal discount
    #     """
    #     for rec in self:
    #         if not rec.ks_global_discount_rate or not rec.ks_global_discount_type:
    #             continue
    #         order_line_with_taxes = rec.invoice_line_ids.filtered(lambda r: not r.display_type and not r.is_downpayment and r.tax_ids)
    #         if len(rec.invoice_line_ids) <= 1 or not order_line_with_taxes:
    #             continue
    #         tax_ids = order_line_with_taxes[0].tax_ids
    #         for line in rec.invoice_line_ids.filtered(lambda r: not r.display_type and not r.is_downpayment):
    #             if line.tax_ids != tax_ids:
    #                 raise ValidationError(_('All order details should have the same taxes or all of them should have not taxes.'))
                    
    
    # def _recompute_tax_lines(self, recompute_tax_base_amount=False, tax_rep_lines_to_recompute=None):
    #     """ Compute the dynamic tax lines of the journal entry.

    #     :param recompute_tax_base_amount: Flag forcing only the recomputation of the `tax_base_amount` field.
    #     """
    #     self.ensure_one()
    #     in_draft_mode = self != self._origin

    #     def _serialize_tax_grouping_key(grouping_dict):
    #         ''' Serialize the dictionary values to be used in the taxes_map.
    #         :param grouping_dict: The values returned by '_get_tax_grouping_key_from_tax_line' or '_get_tax_grouping_key_from_base_line'.
    #         :return: A string representing the values.
    #         '''
    #         return '-'.join(str(v) for v in grouping_dict.values())

    #     def _compute_base_line_taxes(base_line):
    #         ''' Compute taxes amounts both in company currency / foreign currency as the ratio between
    #         amount_currency & balance could not be the same as the expected currency rate.
    #         The 'amount_currency' value will be set on compute_all(...)['taxes'] in multi-currency.
    #         :param base_line:   The account.move.line owning the taxes.
    #         :return:            The result of the compute_all method.
    #         '''
    #         move = base_line.move_id

    #         if move.is_invoice(include_receipts=True):
    #             handle_price_include = True
    #             sign = -1 if move.is_inbound() else 1
    #             quantity = base_line.quantity
    #             is_refund = move.move_type in ('out_refund', 'in_refund')
    #             price_unit_wo_discount = sign * base_line.price_unit * (1 - (base_line.discount / 100.0))
    #             if move.ks_global_discount_rate and  move.ks_amount_discount:
    #                quantity = 1
    #                amount = move.amount_untaxed
    #                downpayment_line = move.line_ids.filtered(lambda r: not r.exclude_from_invoice_tab and r.is_downpayment)
    #                if downpayment_line:
    #                    other_lines = move.line_ids.filtered(lambda r: not r.exclude_from_invoice_tab) - downpayment_line
    #                    amount = sum(line.price_subtotal for line in other_lines)
    #                    amount -= move.ks_amount_discount
    #                price_unit_wo_discount =  sign * amount
                    
    #         else:
    #             handle_price_include = False
    #             quantity = 1.0
    #             tax_type = base_line.tax_ids[0].type_tax_use if base_line.tax_ids else None
    #             is_refund = (tax_type == 'sale' and base_line.debit) or (tax_type == 'purchase' and base_line.credit)
    #             price_unit_wo_discount = base_line.amount_currency

    #         return base_line.tax_ids._origin.with_context(force_sign=move._get_tax_force_sign()).compute_all(
    #             price_unit_wo_discount,
    #             currency=base_line.currency_id,
    #             quantity=quantity,
    #             product=base_line.product_id,
    #             partner=base_line.partner_id,
    #             is_refund=is_refund,
    #             handle_price_include=handle_price_include,
    #             include_caba_tags=move.always_tax_exigible,
    #         )

    #     taxes_map = {}

    #     # ==== Add tax lines ====
    #     to_remove = self.env['account.move.line']
    #     for line in self.line_ids.filtered('tax_repartition_line_id'):
    #         grouping_dict = self._get_tax_grouping_key_from_tax_line(line)
    #         grouping_key = _serialize_tax_grouping_key(grouping_dict)
    #         if grouping_key in taxes_map:
    #             # A line with the same key does already exist, we only need one
    #             # to modify it; we have to drop this one.
    #             to_remove += line
    #         else:
    #             taxes_map[grouping_key] = {
    #                 'tax_line': line,
    #                 'amount': 0.0,
    #                 'tax_base_amount': 0.0,
    #                 'grouping_dict': False,
    #             }
    #     if not recompute_tax_base_amount:
    #         self.line_ids -= to_remove

    #     line_taxes = self.line_ids.filtered(lambda line: not line.tax_repartition_line_id)
    #     uni_line_taxes = self.line_ids.filtered(lambda line: not line.tax_repartition_line_id and line.tax_ids)
    #     if self.ks_global_discount_rate and self.ks_enable_discount and uni_line_taxes:
    #         line_taxes = uni_line_taxes[0]
            
    #     # ==== Mount base lines ====
    #     for line in line_taxes:
    #         # Don't call compute_all if there is no tax.
    #         if not line.tax_ids:
    #             if not recompute_tax_base_amount:
    #                 line.tax_tag_ids = [(5, 0, 0)]
    #             continue

    #         compute_all_vals = _compute_base_line_taxes(line)

    #         # Assign tags on base line
    #         if not recompute_tax_base_amount:
    #             line.tax_tag_ids = compute_all_vals['base_tags'] or [(5, 0, 0)]

    #         for tax_vals in compute_all_vals['taxes']:
    #             grouping_dict = self._get_tax_grouping_key_from_base_line(line, tax_vals)
    #             grouping_key = _serialize_tax_grouping_key(grouping_dict)

    #             tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_vals['tax_repartition_line_id'])
    #             tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id

    #             taxes_map_entry = taxes_map.setdefault(grouping_key, {
    #                 'tax_line': None,
    #                 'amount': 0.0,
    #                 'tax_base_amount': 0.0,
    #                 'grouping_dict': False,
    #             })
    #             taxes_map_entry['amount'] += tax_vals['amount']
    #             taxes_map_entry['tax_base_amount'] += self._get_base_amount_to_display(tax_vals['base'], tax_repartition_line, tax_vals['group'])
    #             taxes_map_entry['grouping_dict'] = grouping_dict

    #     # ==== Pre-process taxes_map ====
    #     taxes_map = self._preprocess_taxes_map(taxes_map)

    #     # ==== Process taxes_map ====
    #     for taxes_map_entry in taxes_map.values():
    #         # The tax line is no longer used in any base lines, drop it.
    #         if taxes_map_entry['tax_line'] and not taxes_map_entry['grouping_dict']:
    #             if not recompute_tax_base_amount:
    #                 self.line_ids -= taxes_map_entry['tax_line']
    #             continue

    #         currency = self.env['res.currency'].browse(taxes_map_entry['grouping_dict']['currency_id'])

    #         # Don't create tax lines with zero balance.
    #         if currency.is_zero(taxes_map_entry['amount']):
    #             if taxes_map_entry['tax_line'] and not recompute_tax_base_amount:
    #                 self.line_ids -= taxes_map_entry['tax_line']
    #             continue

    #         # tax_base_amount field is expressed using the company currency.
    #         tax_base_amount = currency._convert(taxes_map_entry['tax_base_amount'], self.company_currency_id, self.company_id, self.date or fields.Date.context_today(self))

    #         # Recompute only the tax_base_amount.
    #         if recompute_tax_base_amount:
    #             if taxes_map_entry['tax_line']:
    #                 taxes_map_entry['tax_line'].tax_base_amount = tax_base_amount
    #             continue

    #         balance = currency._convert(
    #             taxes_map_entry['amount'],
    #             self.company_currency_id,
    #             self.company_id,
    #             self.date or fields.Date.context_today(self),
    #         )
    #         to_write_on_line = {
    #             'amount_currency': taxes_map_entry['amount'],
    #             'currency_id': taxes_map_entry['grouping_dict']['currency_id'],
    #             'debit': balance > 0.0 and balance or 0.0,
    #             'credit': balance < 0.0 and -balance or 0.0,
    #             'tax_base_amount': tax_base_amount,
    #         }

    #         if taxes_map_entry['tax_line']:
    #             # Update an existing tax line.
    #             if tax_rep_lines_to_recompute and taxes_map_entry['tax_line'].tax_repartition_line_id not in tax_rep_lines_to_recompute:
    #                 continue

    #             taxes_map_entry['tax_line'].update(to_write_on_line)
    #         else:
    #             # Create a new tax line.
    #             create_method = in_draft_mode and self.env['account.move.line'].new or self.env['account.move.line'].create
    #             tax_repartition_line_id = taxes_map_entry['grouping_dict']['tax_repartition_line_id']
    #             tax_repartition_line = self.env['account.tax.repartition.line'].browse(tax_repartition_line_id)

    #             if tax_rep_lines_to_recompute and tax_repartition_line not in tax_rep_lines_to_recompute:
    #                 continue

    #             tax = tax_repartition_line.invoice_tax_id or tax_repartition_line.refund_tax_id
    #             taxes_map_entry['tax_line'] = create_method({
    #                 **to_write_on_line,
    #                 'name': tax.name,
    #                 'move_id': self.id,
    #                 'company_id': self.company_id.id,
    #                 'company_currency_id': self.company_currency_id.id,
    #                 'tax_base_amount': tax_base_amount,
    #                 'exclude_from_invoice_tab': True,
    #                 **taxes_map_entry['grouping_dict'],
    #             })

    #         if in_draft_mode:
    #             taxes_map_entry['tax_line'].update(taxes_map_entry['tax_line']._get_fields_onchange_balance(force_computation=True))

    
    # def _recompute_dynamic_lines(self, recompute_all_taxes=False, recompute_tax_base_amount=False):
    #     """_summary_

    #     Args:
    #         recompute_all_taxes (bool, optional): _description_. Defaults to False.
    #         recompute_tax_base_amount (bool, optional): _description_. Defaults to False.
    #     """
    #     self._recompute_universal_discount_lines()
    #     print("@@@@@@@@@@@@@@@@@ universal 22222222222222222")
    #     return super(KsGlobalDiscountInvoice,self)._recompute_dynamic_lines(recompute_all_taxes, recompute_tax_base_amount)
    
    # @api.model
    # def _get_tax_totals(self, partner, tax_lines_data, amount_total, amount_untaxed, currency):
    #     """
    #     """
    #     res = super(KsGlobalDiscountInvoice,self)._get_tax_totals(partner, tax_lines_data, amount_total, amount_untaxed, currency)
    #     print ("-self._context",self._context)
    #     if 'universal_discount' in self._context:
            
    #         res['amount_untaxed'] = res['amount_untaxed'] - self._context.get('universal_discount')
    #         if res['subtotals']:
    #             amount = res['subtotals'][0]['amount'] - self._context.get('universal_discount')
    #             res['subtotals'][0] = {
    #             'name': res['subtotals'][0]['name'],
    #             'amount': amount ,
    #             'formatted_amount': formatLang(self.env, amount, currency_obj=currency),
    #             }
    #         res['formatted_amount_untaxed'] = formatLang(self.env, res['amount_untaxed'] - self._context.get('universal_discount'), currency_obj=currency)
    #     return res
    
    # @api.depends('line_ids.amount_currency', 'line_ids.tax_base_amount', 'line_ids.tax_line_id', 'partner_id', 'currency_id', 'amount_total', 'amount_untaxed')
    # def _compute_tax_totals_json(self):
    #     """ Computed field used for custom widget's rendering.
    #         Only set on invoices.
    #     """
    #     not_universal_order = self.filtered(lambda r: not r.ks_global_discount_rate or not r.ks_global_discount_type or not r.invoice_line_ids.filtered(lambda s: s.tax_ids))
    #     super(KsGlobalDiscountInvoice, not_universal_order)._compute_tax_totals_json()
    #     for move in (self - not_universal_order):
    #         if not move.is_invoice(include_receipts=True):
    #             # Non-invoice moves don't support that field (because of multicurrency: all lines of the invoice share the same currency)
    #             move.tax_totals_json = None
    #             continue

    #         tax_lines_data = move._prepare_tax_lines_data_for_totals_from_invoice()

    #         move.tax_totals_json = json.dumps({
    #             **self.with_context({'universal_discount': move.ks_amount_discount})._get_tax_totals(move.partner_id, tax_lines_data, move.amount_total, move.amount_untaxed, move.currency_id),
    #             'allow_tax_edition': move.is_purchase_document(include_receipts=False) and move.state == 'draft',
    #         })
            
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    is_downpayment = fields.Boolean(
        string="Is a down payment", help="Down payments are made when creating invoices from a sales order."
        " They are not copied when duplicating a sales order.", default=False)
    
    tax_amount = fields.Monetary(string='Tax Amount', store=False, readonly=True,
        currency_field='currency_id', compute='_compute_tax_amount')
    
    # @api.depends('price_total', 'price_subtotal', 'move_id.special_discount', 'move_id.ks_amount_discount')
    # def _compute_tax_amount(self):
    #     for rec in self:
    #         line_discount_price_unit = rec.price_unit * (1 - (rec.discount / 100.0))
    #         rate = rec.move_id.get_universal_discount_rate()
    #         line_discount_price_unit = line_discount_price_unit * (1 - (rate / 100.0))
    #         rec.tax_amount = rec.price_total - line_discount_price_unit * rec.quantity
    #         if rec.is_downpayment:
    #             rec.tax_amount = 0
    
    # @api.model
    # def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
    #     ''' This method is used to compute 'price_total' & 'price_subtotal'.

    #     :param price_unit:  The current price unit.
    #     :param quantity:    The current quantity.
    #     :param discount:    The current discount.
    #     :param currency:    The line's currency.
    #     :param product:     The line's product.
    #     :param partner:     The line's partner.
    #     :param taxes:       The applied taxes.
    #     :param move_type:   The type of the move.
    #     :return:            A dictionary containing 'price_subtotal' & 'price_total'.
    #     '''
    #     res = super(AccountMoveLine, self)._get_price_total_and_subtotal_model(price_unit, quantity, discount, currency, product, partner, taxes, move_type)
    #     # Adding universal dicount
    #     if taxes and self.move_id.ks_amount_discount and 'price_total' in res:
    #         line_discount_price_unit = price_unit * (1 - (discount / 100.0))
    #         # subtotal = quantity * line_discount_price_unit
    #         rate = self.move_id.get_universal_discount_rate()
    #         line_discount_price_unit = line_discount_price_unit * (1 - (rate / 100.0))
    #         taxes_res = taxes._origin.with_context(force_sign=1).compute_all(line_discount_price_unit,
    #             quantity=quantity, currency=currency, product=product, partner=partner, is_refund=move_type in ('out_refund', 'in_refund'))
    #         # res['price_subtotal'] = taxes_res['total_excluded']
    #         res['price_total'] = taxes_res['total_included']
        
    #     #In case of multi currency, round before it's use for computing debit credit
    #     if currency:
    #         res = {k: currency.round(v) for k, v in res.items()}
        
    #     return res
