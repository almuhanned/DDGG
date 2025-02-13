from odoo import api, fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    appears_on_report = fields.Boolean(string="Appears on Report")
