# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PayrollReportWizard(models.TransientModel):
    _name = 'payroll.report.wizard'
    _description = 'Payroll Report Wizard'

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    salary_structure_id = fields.Many2one('hr.payroll.structure', string="Salary Structure")

    def print_xls_report(self):
        data = {'form': self.read()[0]}
        all_payslip_data = self.get_employee_payslip()
        if not all_payslip_data:
            raise ValidationError(_("No Data ..."))
        data.update({'payslip_ids': all_payslip_data})
        return self.env.ref('payroll_report.action_report_payroll_batch').report_action(self, data=data)

    def get_employee_payslip(self):
        payslips = []
        domain = [('date_from', '>=', self.from_date), ('struct_id', '=', self.salary_structure_id.id)]
        if self.to_date:
            domain.append(('date_from', '<=', self.to_date))
        payslip_ids = self.env['hr.payslip'].search(domain)
        if payslip_ids:
            payslips = payslip_ids.ids
        return payslips
