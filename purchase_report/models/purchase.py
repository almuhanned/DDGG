
from odoo import _, api, exceptions, fields, models
from datetime import datetime, timedelta


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    sale_id = fields.Many2one('sale.order',string="Sales Order No.")
    sale_date = fields.Datetime(string="Sales Order Date")
    sale_employee = fields.Many2one('hr.employee',string="Sales Employees")
    street = fields.Char(related="company_id.street")
    street2 = fields.Char(related="company_id.street2")
    city = fields.Char(related="company_id.city")
    state_id = fields.Many2one('res.country.state',related="company_id.state_id")
    zip_f = fields.Char(related="company_id.zip")
    country_id = fields.Many2one('res.country',related="company_id.country_id")
    amount_in_word = fields.Char(compute="_compute_amount_in_word")
    approved_by = fields.Many2one('res.users')
    approve_date = fields.Datetime(string="Approve Date")

    contact_phone_Delivery = fields.Char(string="Phone", related="sale_employee.mobile_phone")
    contact_email_Delivery = fields.Char(string="Email", related="sale_employee.work_email")

    def _compute_amount_in_word(self):
        self.amount_in_word = ''
        amount_in_words = self.currency_id.with_context(lang=self.partner_id.lang or 'es_ES').amount_to_text(self.amount_untaxed)
        self.amount_in_word = amount_in_words


    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        self.approved_by = self.env.user
        self.approve_date = fields.Datetime.now()
        return res
