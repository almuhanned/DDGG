# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    salesperson = fields.Many2one("hr.employee", default=_get_employee_id, string="Salesperson", tracking=True)


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_employee_id(self):
        employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        return employee_rec.id

    salesperson = fields.Many2one("hr.employee", default=_get_employee_id, string="Salesperson", tracking=True)

    invoice_type = fields.Selection([("cash_invoice", "Cash Invoice"), ("aged_invoice", "Aged Invoice"),
                                     ("maintenance_invoice", "Maintenance Invoice"),
                                     ], "Invoice Type", default="cash_invoice", )
