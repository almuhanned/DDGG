from odoo import models, fields, api
from datetime import timedelta, datetime


class HolidaysRequest(models.Model):
    _inherit = "hr.leave"

    def action_validate(self):
        res = super(HolidaysRequest, self).action_validate()
        for record in self:
            if record.holiday_status_id.including_weekend:
                # Get the start and end dates of the time off
                start_date = record.date_from
                end_date = record.date_to

                # Create work entries for each day including weekends
                current_date = start_date
                while current_date <= end_date:
                    # Check if the current date is a Friday or Saturday
                    if current_date.weekday() in [4, 5]:  # 4 = Friday, 5 = Saturday
                        # Define the start and end time for the work entry
                        date_start = datetime.combine(current_date, datetime.strptime("06:00:00", "%H:%M:%S").time())
                        date_end = datetime.combine(current_date, datetime.strptime("14:00:00", "%H:%M:%S").time())
                        self.sudo().env['hr.work.entry'].create({
                            'name': "%s: %s" % (record.holiday_status_id.work_entry_type_id.name, record.employee_id.name),
                            'employee_id': record.employee_id.id,
                            'date_start': date_start,
                            'date_stop': date_end,
                            'work_entry_type_id': record.holiday_status_id.work_entry_type_id.id,
                            'state': 'draft',
                            'contract_id': record.employee_id.contract_id.id,
                            'company_id': record.employee_id.contract_id.company_id.id,
                            'duration': 8,
                            'leave_id': record.id,
                            # Reference to your work entry type
                        })
                    current_date += timedelta(days=1)
        return res


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    including_weekend = fields.Boolean(string="Including Weekend", default=False, help="This leave including weekend.")


class HrWorkEntry(models.Model):
    _inherit = 'hr.work.entry'

    def _check_if_error(self):
        if not self:
            return False
        undefined_type = self.filtered(lambda b: not b.work_entry_type_id)
        undefined_type.write({'state': 'conflict'})
        for work_entry_type_id in self.work_entry_type_id:
            if work_entry_type_id.id == 5:
                return True
        conflict = self._mark_conflicting_work_entries(min(self.mapped('date_start')), max(self.mapped('date_stop')))
        return undefined_type or conflict

    def _get_duration(self, date_start, date_stop):
        if not date_start or not date_stop:
            return 0
        if self.work_entry_type_id.id == 5:
            return 8
        if self._get_duration_is_valid():
            calendar = self.contract_id.resource_calendar_id
            if not calendar:
                return 0
            employee = self.contract_id.employee_id
            contract_data = employee._get_work_days_data_batch(
                date_start, date_stop, compute_leaves=False, calendar=calendar
            )[employee.id]
            return contract_data.get('hours', 0)
        return super()._get_duration(date_start, date_stop)