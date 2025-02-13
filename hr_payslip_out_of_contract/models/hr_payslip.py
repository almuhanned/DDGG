# -*- coding: utf-8 -*-


from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class HrPayroll(models.Model):
    _inherit = 'hr.payslip'

    def _get_worked_day_lines(self, domain=None, check_out_of_contract=True):
        """
        :returns: a list of dict containing the worked days values that should be applied for the given payslip
        """
        res = super(HrPayroll, self)._get_worked_day_lines(domain=domain, check_out_of_contract=check_out_of_contract)

        if self.env.company.allow_out_of_contract_weekend:
            work_entry_type_ids = [line.get('work_entry_type_id') for line in res]
            out_of_contract_work_entry_type_id = self.env.ref('hr_payroll.hr_work_entry_type_out_of_contract')
            if out_of_contract_work_entry_type_id.id in work_entry_type_ids:
                out_days, out_hours = self.get_out_of_contract_data(self.contract_id)
                for line in res:
                    if line.get('work_entry_type_id') == out_of_contract_work_entry_type_id.id:
                        line.update({
                            'number_of_days': out_days,
                            'number_of_hours': out_hours,
                        })
        return res

    def get_out_of_contract_data(self, contract):
        # If the contract doesn't cover the whole month, create
        # worked_days lines to adapt the wage accordingly
        out_days, out_hours = 0, 0
        reference_calendar = self._get_out_of_contract_calendar()
        if self.date_from < contract.date_start:
            start = fields.Datetime.to_datetime(self.date_from)
            stop = fields.Datetime.to_datetime(contract.date_start)
            delta = stop - start
            out_days += delta.days
            out_hours += reference_calendar.hours_per_day * out_days
        if contract.date_end and contract.date_end < self.date_to:
            start = fields.Datetime.to_datetime(contract.date_end)
            stop = fields.Datetime.to_datetime(self.date_to)
            delta = stop - start
            out_days += delta.days
            out_hours += reference_calendar.hours_per_day * out_days
        return out_days, out_hours
