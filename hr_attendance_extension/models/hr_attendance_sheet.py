# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
import datetime
import pytz
from odoo.tools.misc import format_date


class HrAttendanceSheet(models.Model):
    _name = 'hr.attendance.sheet'
    _description = 'HR Attendance Sheet'

    name = fields.Char(struct='Name', compute='_compute_name', store=True, )
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirmed'),
                              ('approve', 'Approve'), ('cancel', 'Cancel')], default='draft', string='State')

    line_ids = fields.One2many('hr.attendance.sheet.line', 'sheet_id', string='Lines')
    deducted = fields.Boolean(string='Deducted')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    @api.depends('date_from')
    def _compute_name(self):
        for sheet in self.filtered(lambda p: p.date_from):
            lang = self.env.user.lang
            context = {'lang': lang}
            sheet_name = _('Attendance Sheet')
            del context
            sheet.name = '%(sheet_name)s - %(dates)s' % {
                'sheet_name': sheet_name,
                'dates': format_date(self.env, sheet.date_from, date_format="MMMM y", lang_code=lang)
            }

    def compute_attendance(self):
        sheet_period = self.get_days_and_names(self.date_from,self.date_to)
        self.line_ids = None
        employees = self.env['hr.employee'].search([])
        lines = []
        attendance_dict = {}
        for emp in employees:
            calendar_id = emp.resource_calendar_id
            emp_planned_hours = 0
            emp_act_hours = 0
            emp_absence_days = 0
            attendance = self.env['hr.attendance'].search([('employee_id', '=', emp.id)])
            attendance = attendance.filtered(
                lambda a: self.date_from <= a.check_in.date() <= self.date_to)
            act_hours = sum(attendance.mapped('worked_hours')) or 0.0
            late_in = sum(attendance.mapped('late_in')) or 0.0
            early_exit = sum(attendance.mapped('early_exit')) or 0.0
            diff_time = sum(attendance.mapped('diff_time')) or 0.0
            overtime = sum(attendance.mapped('overtime')) or 0.0
            late = str(late_in).split('.')
            early = str(early_exit).split('.')
            minutes = ((int(late[0]) + int(early[0])) * 60) + int(late[1][:2]) + int(early[1][:2])


            emp_working_days = calendar_id.attendance_ids.mapped('dayofweek')
            # calculate employee planned hours within selected period
            for period_day in sheet_period :
                emp_work_days = calendar_id.attendance_ids.filtered(lambda a: a.dayofweek == str(sheet_period[period_day]))
                working_hours = sum([(day.hour_to - day.hour_from) for day in emp_work_days])   
                emp_planned_hours +=  working_hours     
                check_attendance = attendance.filtered(lambda a: period_day  == a.check_in.date())  
                if str(sheet_period[period_day]) in emp_working_days and not check_attendance :
                    emp_absence_days += 1
                if check_attendance :
                    emp_act_hours += sum(check_attendance.mapped('worked_hours'))
               
            new_line = {
                'employee_id': emp.id,
                'planned_hours': emp_planned_hours,
                'act_hours': emp_act_hours,
                'late_in': late_in,
                'early_exit': early_exit,
                'diff_time': diff_time,
                'overtime': overtime,
                'absence_days': emp_absence_days,
                'deduction_amount': minutes* ((((emp.contract_id.wage)/30)/calendar_id.hours_per_day)/60)
            }

            lines.append((0, 0, new_line))

        self.write({'line_ids': lines})

    def get_days_and_names(self,start_date, end_date):
        """
        Returns a dictionary containing days and their corresponding day names for the given period.
        """
        days_and_names = {}
        delta = datetime.timedelta(days=1)
        while start_date <= end_date:
            day_name = start_date.weekday()
            days_and_names[start_date] = day_name
            start_date += delta
        return days_and_names

    def action_confirm(self):
        self.state = 'confirm'

    def action_approve(self):
        self.state = 'approve'

    def action_cancel(self):
        self.state = 'cancel'


class HrAttendanceLines(models.Model):
    _name = 'hr.attendance.sheet.line'

    employee_id = fields.Many2one('hr.employee', readonly=0)
    planned_hours = fields.Float(string='PL-Hours', readonly=0)
    act_hours = fields.Float(string='ACT-Hours', readonly=0)
    absence_days = fields.Integer(string='Absence Days', readonly=0)
    late_in = fields.Float(string='Late In', readonly=0)
    early_exit = fields.Float(string='Early Exit', readonly=0)
    diff_time = fields.Float(string='Diff Time', readonly=0)
    overtime = fields.Float(string='OverTime', readonly=0)
    deduction_amount = fields.Float(string='Deduction Amount')
    sheet_id = fields.Many2one('hr.attendance.sheet', ondelete='cascade')

    # @api.depends('employee_id')
    # def compute_hours(self):
    #     for line in self:
    #         attendance = self.env['hr.attendance'].search([('employee_id', '=', line.employee_id.id)])
    #         attendance = attendance.filtered(lambda a: line.sheet_id.date_from <= a.check_in.date() <= line.sheet_id.date_to)
    #         line. act_hours = sum(attendance.mapped('worked_hours'))
    #         line. late_in = sum(attendance.mapped('late_in'))
    #         line. early_exit = sum(attendance.mapped('early_exit'))
    #         line. diff_time = sum(attendance.mapped('diff_time'))
    #         line.overtime = sum(attendance.mapped('overtime'))

    @api.depends('employee_id')
    def compute_absence_days(self):
        for line in self:
            attendance = self.env['hr.attendance'].search([('employee_id', '=', line.employee_id.id)])
            attendances = attendance.filtered(
                lambda a: line.sheet_id.date_from <= a.check_in.date() <= line.sheet_id.date_to)
            calendar_id = line.employee_id.resource_calendar_id
            attendance_day = calendar_id.attendance_ids.mapped('dayofweek')
            day_generator = (line.sheet_id.date_from + datetime.timedelta(x + 1) for x in range(
                (line.sheet_id.date_to - line.sheet_id.date_from).days))
            delta_days = sum(1 for day in day_generator if str(day.weekday()) in attendance_day)
            line.absence_days = delta_days - len(attendances)


