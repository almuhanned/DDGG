from odoo import models,api,fields,_


class HrOverTimeTypeExt(models.Model):
    _inherit = 'overtime.type'

    payslip_input_type_id = fields.Many2one('hr.payslip.input.type', 'Other Input')
    rate = fields.Float(string='Rate')
    hour_limited = fields.Float(string='Hour Limited')