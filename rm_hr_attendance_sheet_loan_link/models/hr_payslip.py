# -*- coding: utf-8 -*-

from odoo import models, api, fields, Command
# from odoo.addons.rm_hr_attendance_sheet.models.hr_payslip import HrPayslipInherit

from datetime import datetime, date, timedelta


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def get_loan_installment(self, payslip):
        installments = []
        installment_ids = self.env['installment.line'].search([('employee_id', '=', payslip.employee_id.id), ('loan_id.state', '=', 'done'), ('is_paid', '=', False), ('date', '<=', payslip.date_to)])
        if installment_ids:
            installments = installment_ids.ids
        return installments

    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        for payslip in self:
            installments = payslip.get_loan_installment(payslip)
            if installments:
                payslip.write({'installment_ids': [(6, 0, installments)]})
        return res
