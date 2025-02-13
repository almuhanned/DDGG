from odoo import api, fields, models
from datetime import date, timedelta
from pytz import timezone
from datetime import date, timedelta
from datetime import date, datetime, time


class HrPayslipInherit(models.Model):

    _inherit = 'hr.payslip'

    def compute_sheet(self):
        res = super(HrPayslipInherit, self).compute_sheet()
        for rec in self:
            summ = 0
            summ1 = 0
            apsense = 0
            tz = timezone(rec.employee_id.resource_calendar_id.tz)

            date_from = tz.localize(datetime.combine(fields.Datetime.from_string(str(rec.date_from)), time.min))
            date_to = tz.localize(datetime.combine(fields.Datetime.from_string(str(rec.date_to)), time.max))

            delta = date_to - date_from
            for i in range(delta.days + 1):
                day = date_from + timedelta(days=i)
                # print(day.date())
                print(day.date())
                attendances = self.env["hr.attendance"].search(
                    [('employee_id', '=', rec.employee_id.id), ('check_in', '=', str(day.date()))
                     ])
                if not attendances:
                    apsense += 1
            print(apsense)

        # late_obj1 = self.env["hr.attendance"].search(
        #     [('employee_id', '=', self.employee_id.id), ('check_out', '>=', self.date_from),
        #      ('check_out', '<=', self.date_to)])
        # late_obj = self.env['late.check_in'].search(
        #     [('employee_id', '=', self.employee_id.id), ('date', '>=', self.date_from), ('date', '<=', self.date_to)])
        # for re in late_obj1:
        #     if re.late_check_in>10 and re.late_check_in !=0 :
        #         print("-------------")
        #         print(summ,"sum")
        #         print(re.late_check_in,"re.late_check_in")
        #
        #
        #         summ = summ+re.late_check_in*5
        #         print(summ , "sum after")


            rec.employee_id.latee = summ


            #if late_obj:
             #   for recc in late_obj:
              #      if recc.late_minutes>10:

                      #  summ += recc.late_minutes*5
            #self.employee_id.latee = summ
            # early_leave = self.env["hr.attendance"].search(
            #     [('employee_id', '=', self.employee_id.id), ('check_out', '>=', self.date_from),
            #      ('check_out', '<=', self.date_to)])

            # print(early_leave)
            # if early_leave:
            #     for recc in early_leave:
            #         summ1 += recc.early_check_out
            # self.employee_id.early_leave = summ1

            absent = 0
            delta = rec.date_to - rec.date_from
            flag = False
            for i in range(delta.days + 1):

                day = rec.date_from + timedelta(days=i)

                attendances = rec.env["hr.attendance"].search(
                    [('employee_id', '=', rec.employee_id.id), ('check_in', '=', day)])
                work_hours_sum = 0
                less_than7 = False
                if not attendances:
                    absent += 1
                for att in attendances:
                    if not att.check_out and att.check_in:
                        absent += 1
                    if not att.check_in and att.check_out:
                        absent += 1
                    work_hours_sum += att.worked_hours
                    if att.check_out:
                        flag = True

                if 8 >= work_hours_sum >= 7:
                    less_than7 = True
                if attendances and flag:
                    if less_than7:
                        absent += .5
                if absent > 4:
                    rec.employee_id.days_latee = absent-4
        for payslip in self.filtered(lambda slip: slip.state in ['draft', 'verify']):
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            lines = [(0, 0, line) for line in payslip._get_payslip_lines()]
            payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today()})
        return res
