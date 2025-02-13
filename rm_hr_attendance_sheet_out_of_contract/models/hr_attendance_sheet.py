# -*- coding: utf-8 -*-

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta


class AttendanceSheet(models.Model):
    _inherit = 'attendance.sheet'

    number_out_contract = fields.Integer(string="Number Out of Contract", compute="compute_number_out_contract", store=True)

    @api.depends('line_ids', 'line_ids.status')
    def compute_number_out_contract(self):
        """
            Compute out of contract number
        """
        for rec in self:
            number_out_contract = 0
            if rec.line_ids:
                line_ids = rec.line_ids.filtered(lambda line: line.status == 'out_contract')
                number_out_contract = len(line_ids)
            rec.number_out_contract = number_out_contract

    def get_attendances(self):
        """
            Inherit get attendance lines function to add out of contract lines
        """
        res = super(AttendanceSheet, self).get_attendances()
        for rec in self:
            if rec.line_ids:
                if rec.date_from < rec.contract_id.date_start:
                    start = datetime.strptime(str(rec.date_from), "%Y-%m-%d")
                    stop = datetime.strptime(str(rec.contract_id.date_start), "%Y-%m-%d")
                    delta = relativedelta(stop, start)
                    print("DELATA ==========", delta.days)
                    for i in range(delta.days):
                        print("I ==", i)
                        date = start + relativedelta(days=i)
                        print("DATE =====", date.date())
                        attendance_sheet_line_id = rec.line_ids.filtered(lambda line: line.date == date.date())
                        print("attendance_sheet_line_id=======", attendance_sheet_line_id)
                        if attendance_sheet_line_id:
                            print("LINES DAT", attendance_sheet_line_id.date, "STATE ==", attendance_sheet_line_id.status)

                            attendance_sheet_line_id.sudo().write({
                                'status': 'out_contract'
                            })
        return res


class AttendanceSheetLine(models.Model):
    _inherit = 'attendance.sheet.line'

    status = fields.Selection(selection_add=[('out_contract', 'Out of Contract')])
