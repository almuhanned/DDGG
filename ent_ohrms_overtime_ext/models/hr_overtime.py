from dateutil import relativedelta
import pandas as pd
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError



class HrOverTimeExt(models.Model):
    _inherit = 'hr.overtime'
    _description = "HR Overtime"

    hr_responsible_id = fields.Many2one('res.users', string="HR Responsible", related="contract_id.hr_responsible_id", store=True)

    @api.depends('date_from', 'date_to', 'duration_type')
    def _get_days(self):
        for recd in self:
            if recd.date_from and recd.date_to:
                if recd.date_from > recd.date_to:
                    raise ValidationError('Start Date must be less than End Date')
        for sheet in self:
            if sheet.date_from and sheet.date_to:
                start_dt = fields.Datetime.from_string(sheet.date_from)
                finish_dt = fields.Datetime.from_string(sheet.date_to)

                # Calculate difference
                difference = relativedelta.relativedelta(finish_dt, start_dt)
                s = finish_dt - start_dt
                days_in_mins = s.days * 24 * 60
                hours_in_mins = difference.hours * 60
                total_minutes = days_in_mins + hours_in_mins + difference.minutes
                days_no = total_minutes / (24 * 60)

                # Calculate the hours and days
                diff = finish_dt - start_dt
                total_hours = diff.days * 24 + diff.seconds // 3600
                remaining_minutes = (diff.seconds % 3600) // 60

                average_minutes = round(remaining_minutes / 60, 2)

                if sheet.duration_type == 'hours':
                    sheet.days_no_tmp = total_hours + average_minutes
                elif sheet.duration_type == 'days':
                    sheet.days_no_tmp = days_no

    @api.constrains('days_no_tmp')
    def overtime_hour_limited(self):
        for record in self:
            if record.type in ['cash', 'leave']:
                if record.overtime_type_id.hour_limited < record.days_no_tmp:
                    raise ValidationError(
                        _("The number of hours cannot exceed the limited hours set for overtime."))

    @api.onchange('overtime_type_id')
    def _get_hour_amount(self):
        if self.duration_type == 'hours':
            if self.contract_id and self.contract_id.over_hour:
                cash_amount = self.days_no_tmp * self.contract_id.over_hour * self.overtime_type_id.rate
                self.cash_hrs_amount = cash_amount
            else:
                raise UserError(_("Hour Overtime Needs Hour Wage in Employee Contract."))
        elif self.duration_type == 'days':
            if self.contract_id and self.contract_id.over_day:
                cash_amount = self.days_no_tmp * self.contract_id.over_day * self.overtime_type_id.rate
                self.cash_day_amount = cash_amount
            else:
                raise UserError(_("Day Overtime Needs Day Wage in Employee Contract."))

    def approve(self):
        if self.contract_id.hr_responsible_id != self.env.user:
            raise UserError(_("Only the hr responsible for this employee can approve this request."))
        return super(HrOverTimeExt, self).approve()





