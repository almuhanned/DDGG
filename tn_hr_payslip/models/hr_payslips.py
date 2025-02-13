from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from datetime import timedelta, datetime, date
from dateutil import relativedelta

class HRPayslips(models.Model):
    _inherit = 'hr.payslip'

    total_salary = fields.Monetary('Total Salary', currency_field='currency_id', digits=dp.get_precision('Account'), 
                                   compute='compute_total_salary', store=True)

    time_leave_id = fields.Many2one(
        string='Time Off',
        comodel_name='hr.leave',
        compute='compute_time_off_employee' 
    )
    
    @api.depends('employee_id')
    def compute_time_off_employee(self):
        for rec in self:
            time_off_ids = self.env['hr.leave'].search([('employee_id', '=', rec.employee_id.id),('state', '=', 'validate')])
            if time_off_ids:
                if len(time_off_ids) > 1:
                    rec.time_leave_id = time_off_ids[-1].id
                else:
                    rec.time_leave_id = time_off_ids.id
            else:
                rec.time_leave_id = False



    @api.depends('line_ids.total')
    def compute_total_salary(self):
        for payslip in self:
            net = payslip.line_ids.filtered(lambda r: r.code == "NET").total
            if net > 0.0:
                payslip.total_salary = net
            else:
                payslip.total_salary = 0.0
