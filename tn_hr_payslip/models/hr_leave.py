from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    structure_id = fields.Many2one('hr.payroll.structure', string='Structure',domain=[('is_ticket','=',True)], required=False)
            
    def create_payslip_button(self):
        if self.slip_id:
            raise UserError('You already created a payslip, Please delete it first ')
        else:
            count = 0
            for rec in self:
                payslip_obj = rec.env['hr.payslip']
                payslip_name = _('leave and Ticket Salary Slip')
                record_dict = {
                    'employee_id': rec.employee_id.id,
                    'contract_id': rec.contract_id.id,
                    'date_from': rec.request_date_from,
                    'date_to': rec.request_date_to,
                    'struct_id': rec.structure_id.id,
                    'name': '%s - %s' % (payslip_name, self.employee_id.name or ''),
                    'leave_payslip_id': rec.id,
                    'x_studio_is_paid': True
                }

                slip_id = payslip_obj.create(record_dict)
                slip_id.compute_sheet()
                rec.slip_id = slip_id.id
                count += 1
                self.payslip_count = count

  