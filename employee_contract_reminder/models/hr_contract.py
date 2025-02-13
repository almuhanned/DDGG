import logging
from dateutil.relativedelta import relativedelta
from odoo import api, models, fields, _

class HrContract(models.Model):
    _inherit = 'hr.contract'

    @api.model
    def _cron_employee_contract_reminder(self):
        contract_ids = self.get_contracts_to_remind()
        if contract_ids:
            group = self.env.ref('employee_contract_reminder.group_access_contract_expiry_email')
            if group:
                contract_ids.send_mail_reminder()
            else:
                return
            return contract_ids
        else:
            return
        

    @api.model
    def get_contracts_to_remind(self):
        contract_reminder_days = self.env['ir.config_parameter'].sudo().get_param('employee_contract_reminder.contract_reminder_days')
        if not contract_reminder_days:
            return []
        contract_ids = self.search([
            ('state', '=', 'open'),
            ('date_end', '!=', False),
            ('date_end', '>=', fields.Date.today()),
            ('date_end', '<=', fields.Date.today() + relativedelta(days=int(contract_reminder_days)))
        ])
        return contract_ids

    def send_mail_reminder(self):
        template = self.env.ref('employee_contract_reminder.email_template_employee_contract_reminder')
        group = self.env.ref('employee_contract_reminder.group_access_contract_expiry_email')
        email_list = group.users.mapped('email')
        user_ids = group.users.mapped('id')
        for contract in self:
            for user_id in user_ids:
                contract.sudo().activity_schedule('Contract Expiry', user_id=user_id)
            for email in email_list:
                    template.send_mail(contract.id, force_send=True, email_values={'email_to': email})