# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HRPayrollStructure(models.Model):
    _inherit = "hr.payroll.structure"

    is_ticket = fields.Boolean(string='Ticket')
   