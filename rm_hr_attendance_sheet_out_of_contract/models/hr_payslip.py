# -*- coding: utf-8 -*-

from odoo import models, api, fields, Command
# from odoo.addons.rm_hr_attendance_sheet.models.hr_payslip import HrPayslipInherit

from datetime import datetime, date, timedelta


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_overtime_input(self, payslip):
        """
        Get overtime input.

        """
        input_data = []
        overtime_type = self.env.ref('ent_ohrms_overtime.hr_salary_rule_overtime')
        overtime_input_type = self.env.ref('ent_ohrms_overtime.input_overtime_payroll')
        payslip_from_datetime_min = datetime.combine(payslip.date_from, datetime.min.time())
        payslip_to_datetime_max = datetime.combine(payslip.date_to, datetime.max.time())
        overtime_id = self.env['hr.overtime'].search([('date_from', '>=', payslip_from_datetime_min), ('date_to', '<=', payslip_to_datetime_max), ('employee_id', '=', payslip.employee_id.id), ('contract_id', '=', payslip.contract_id.id), ('state', '=', 'approved'), ('payslip_paid', '=', False)])
        if overtime_id:
            hrs_amount = overtime_id.mapped('cash_hrs_amount')
            day_amount = overtime_id.mapped('cash_day_amount')
            cash_amount = sum(hrs_amount) + sum(day_amount)
            old_input_rec = payslip.input_line_ids.filtered(lambda r: r.input_type_id.id == overtime_input_type.id)

            if old_input_rec:
                print(old_input_rec)
                for rec in old_input_rec:
                    payslip.input_line_ids = [(2, rec.id, 0)]

            if overtime_id and payslip.struct_id and overtime_input_type in payslip.struct_id.input_line_type_ids:
                payslip.overtime_ids = overtime_id

                input_data.append(Command.create({
                    'name': overtime_type.name,
                    'amount': cash_amount,
                    'input_type_id': overtime_input_type.id if overtime_input_type else 1
                }))
        return input_data

    def compute_sheet(self):
        res = super(HrPayslip, self).compute_sheet()
        for payslip in self:
            input_data = payslip.get_overtime_input(payslip)
            if input_data:
                payslip.update({'input_line_ids': input_data})
        return res
