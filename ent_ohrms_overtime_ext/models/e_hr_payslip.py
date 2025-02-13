from odoo import models, api, fields, Command
from datetime import datetime, date, timedelta

class PayslipOverTime(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def _compute_input_line_ids(self):
        """
        function used for writing overtime record in payslip
        input tree.

        """
        res = super(PayslipOverTime, self)._compute_input_line_ids()
        for rec in self:
            input_data = []
            overtime_type = self.env.ref('ent_ohrms_overtime.hr_salary_rule_overtime')
            overtime_input_type = self.env.ref('ent_ohrms_overtime.input_overtime_payroll')
            payslip_from_datetime_min = datetime.combine(rec.date_from, datetime.min.time())
            payslip_to_datetime_max = datetime.combine(rec.date_to, datetime.max.time())
            old_input_rec = rec.input_line_ids.filtered(lambda r: r.input_type_id.id == overtime_input_type.id)
            to_remove_vals = [(3, line.id, False) for line in old_input_rec]
            overtime_ids = self.env['hr.overtime'].search([('date_from', '>=', payslip_from_datetime_min), ('date_to', '<=', payslip_to_datetime_max), ('employee_id', '=', rec.employee_id.id), ('contract_id', '=', rec.contract_id.id), ('state', '=', 'approved'), ('payslip_paid', '=', False)])
            if overtime_ids:
                rec.overtime_ids = overtime_ids
                result = {}
                for overtime_id in overtime_ids:
                    if overtime_id.overtime_type_id.name not in result:
                        result[overtime_id.overtime_type_id.name] = {}
                        result[overtime_id.overtime_type_id.name]['lines'] = []
                        result[overtime_id.overtime_type_id.name]['name'] = overtime_id.overtime_type_id.name
                        result[overtime_id.overtime_type_id.name]['input_type'] = overtime_id.overtime_type_id.payslip_input_type_id if overtime_id.overtime_type_id.payslip_input_type_id else overtime_input_type
                    result[overtime_id.overtime_type_id.name]['lines'].append(overtime_id)

                for item in result:
                    if rec.struct_id and overtime_input_type in rec.struct_id.input_line_type_ids:
                        input_data.append((0, 0, ({
                            'name': result[item]['name'],
                            'amount': sum([line.cash_hrs_amount + line.cash_day_amount for line in result[item]['lines']]),
                            # 'input_type_id': overtime_input_type.id if overtime_input_type else 1,
                            'input_type_id': result[item]['input_type'].id
                        })))
            if to_remove_vals:
                input_data += to_remove_vals
            if input_data:
                rec.update({'input_line_ids': input_data})
        return res
