# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    not_show_in_report = fields.Boolean(string="Dont Show In Payslip Report")
