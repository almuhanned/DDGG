from odoo import fields, models, api,_
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def compute_sheet(self):
        for record in self:
            current_month_attendance = self.env['hr.attendance.sheet'].search([('state', '=', 'approve'),
                                                                               ('date_from', '>=', record.date_from),
                                                                               ('date_to', '<=', record.date_to)
                                                                               ])
            if not current_month_attendance:
                raise ValidationError(_("Attendance sheet for %s has not been approved") %(self.date_from).strftime('%B %Y'))
            if record.payslip_run_id:
                self.onchange_employee_get_inputs()
        return super(HrPayslip, self).compute_sheet()

    @api.onchange('employee_id', 'date_from', 'date_to')
    def onchange_employee_get_inputs(self):
        for record in self:
            sheet_id = self.env['hr.attendance.sheet'].search([('state', '=', 'approve'),
                                                               ('date_from', '>=', record.date_from),
                                                               ('date_to', '<=', record.date_to)])
            employee_attendance = sheet_id.line_ids.filtered(lambda line: line.employee_id.id == record.employee_id.id)
            print(employee_attendance)
            input_lines = self.input_line_ids.browse([])
            if employee_attendance:
                # if employee_attendance.overtime:
                #     input_type_id = self.env.ref('hr_attendance_extension.input_overtime')
                #     input_data = {
                #         'name': input_type_id.name,
                #         'code': input_type_id.code,
                #         'amount': employee_attendance.overtime*record.contract_id.over_hour,
                #         'contract_id': record.contract_id.id,
                #         'input_type_id': input_type_id.id,
                #     }
                #     input_lines += input_lines.new(input_data)
                if employee_attendance.late_in or employee_attendance.early_exit:
                    input_type_id = self.env.ref('hr_attendance_extension.input_late_hours')
                    input_data = {
                        'name': input_type_id.name,
                        'code': input_type_id.code,
                        'amount':  employee_attendance.deduction_amount,
                        'contract_id': record.contract_id.id,
                        'input_type_id': input_type_id.id,
                    }
                    input_lines += input_lines.new(input_data)
                record.input_line_ids += input_lines

