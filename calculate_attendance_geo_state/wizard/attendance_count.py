from odoo import fields, models,api,_

class HrAttendanceCount(models.TransientModel):
    _name = "attendance.count.wizard"
    _description = "Attendance Count"

    
    employee_id = fields.Many2one('hr.employee', string="Employee", ondelete='cascade', index=True)
    date_from = fields.Datetime(string="Date From", required=True)
    date_to = fields.Datetime(string="Date To", required=True)



    def print_report_pdf(self):
        id_list = []
        if self.employee_id:
            check_in_count = self.env['hr.attendance'].search_count([('employee_id', '=', self.employee_id.id), '|', ('check_in', '>=', self.date_from), ('check_in', '<=', self.date_to)])
            check_out_count = self.env['hr.attendance'].search_count([('employee_id', '=', self.employee_id.id), '|', ('check_out', '>', self.date_from), ('check_out', '<=', self.date_to)])
            id_list.append({
                        'employee_id': self.employee_id.name,
                        'check_in': check_in_count,
                        'check_out': check_out_count,
                        'id': self.employee_id.id,
                        'email': self.employee_id.work_email,
                        'comp': self.employee_id.company_id.name,
                    })
        else:
            employee_ids = self.env['hr.employee'].search([]).ids
            id_list = []
            for employee in employee_ids:
                    check_in_count = self.env['hr.attendance'].search_count([('employee_id', '=', employee), '|', ('check_in', '>=', self.date_from), ('check_in', '<=', self.date_to)])
                    check_out_count = self.env['hr.attendance'].search_count([('employee_id', '=', employee), '|', ('check_out', '>', self.date_from), ('check_out', '<=', self.date_to)])
                    employee = self.env['hr.employee'].search([('id', '=', employee)])
                    id_list.append({
                        'employee_id': employee.name,
                        'check_in': check_in_count,
                        'check_out': check_out_count,
                        'id': employee.id,
                        'email': employee.work_email,
                        'comp': employee.company_id.name,
                    })
        # print("//////////////////////////////////////////", check_in_count)
        # print("//////////////////////////////////////////", check_out_count)
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_from': self.date_from,
                'date_to': self.date_to,
                'list': id_list,
            },
        }
        return self.env.ref('calculate_attendance_geo_state.user_attendance_print').report_action(self, data=data)

class ReportSaleSummaryReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.calculate_attendance_geo_state.attendance_report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        list = data['form']['list']

        print('XXXXXXXXXXXXX',list)
        return {
            'date_from': date_from,
            'date_to': date_to,
            'list': list,
        }