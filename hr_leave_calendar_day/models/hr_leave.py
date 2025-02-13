# -*- coding: utf-8 -*-

from odoo import models, api, fields, Command
from odoo.addons.resource.models.resource import float_to_time, HOURS_PER_DAY
from datetime import datetime, date, timedelta, time
from odoo.exceptions import AccessError, UserError, ValidationError


class HolidaysRequest(models.Model):
    _inherit = 'hr.leave'

    def _get_number_of_days_calendar(self, date_from, date_to, employee_id):
        if employee_id:
            return self._get_number_of_days_batch_calendar(date_from, date_to, employee_id)[employee_id]
        employee = self.env['hr.employee'].browse(employee_id)
        start = self.date_from
        stop = self.date_to
        delta = stop - start
        today_hours = self.env.company.resource_calendar_id.get_work_hours_count(
            datetime.combine(self.date_from.date(), time.min),
            datetime.combine(self.date_from.date(), time.max),
            False)
        holiday_days = self.get_employee_holiday_days(employee)
        days = delta.days - holiday_days
        hours = days * (today_hours or HOURS_PER_DAY) if not self.request_unit_half else 0.5
        return {'days': days, 'hours': hours}

    def _get_number_of_days_batch_calendar(self, date_from, date_to, employee_ids):
        employee = self.env['hr.employee'].browse(employee_ids)
        # We force the company in the domain as we are more than likely in a compute_sudo
        domain = [('company_id', 'in', self.env.company.ids + self.env.context.get('allowed_company_ids', []))]

        result = employee._get_work_days_data_batch(date_from, date_to, domain=domain)
        start = fields.Datetime.to_datetime(date_from)
        stop = fields.Datetime.to_datetime(date_to)
        delta = stop - start
        today_hours = self.env.company.resource_calendar_id.get_work_hours_count(
            datetime.combine(self.date_from.date(), time.min),
            datetime.combine(self.date_from.date(), time.max),
            False)
        days = delta.days
        hours = days * (today_hours or HOURS_PER_DAY) if not self.request_unit_half else 0.5
        if result:
            for employee_id in result:
                employee = self.env['hr.employee'].browse(employee_id)
                holiday_days = self.get_employee_holiday_days(employee)
                days -= holiday_days
                result[employee_id]['days'] = days
                result[employee_id]['hours'] = hours
                if self.request_unit_half and result[employee_id]['hours'] > 0:
                    result[employee_id]['days'] = 0.5
        return result

    @api.depends('date_from', 'date_to', 'employee_id')
    def _compute_number_of_days(self):
        for holiday in self:
            if not holiday.holiday_status_id.calendar_days:
                super(HolidaysRequest, self)._compute_number_of_days()
            else:
                if holiday.date_from and holiday.date_to:
                    date_to = holiday.date_to + timedelta(days=1)
                    holiday.number_of_days = holiday._get_number_of_days_calendar(holiday.date_from, date_to, holiday.employee_id.id)['days']
                else:
                    holiday.number_of_days = 0

    def get_employee_holiday_days(self, employee):
        holiday_days = 0
        public_holiday_ids = self.env['hr.public.holiday'].search([('state', '=', 'active'), ('date_from', '>=', self.date_from), ('date_to', '<=', self.date_to)])
        employee_public_holiday_ids = [holiday for holiday in public_holiday_ids if employee.id in holiday.emp_ids.ids or employee.department_id.id in holiday.dep_ids.ids or employee.category_ids.ids in holiday.cat_ids.ids]
        if employee_public_holiday_ids:
            for holiday in public_holiday_ids:
                start = fields.Datetime.to_datetime(holiday.date_from)
                stop = fields.Datetime.to_datetime(holiday.date_to) + timedelta(days=1)
                holiday_delta = stop - start
                holiday_days += holiday_delta.days
        return holiday_days


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    calendar_days = fields.Boolean(string="Calendar Days", default=False)
