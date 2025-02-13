from odoo import models, fields, api, exceptions

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_approval_status = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Discount Approval Status", default='pending')

    approval_history = fields.One2many('sale.order.approval.history', 'order_id', string="Approval History")

    @api.constrains('order_line')
    def _check_discount_limit(self):
        for order in self:
            for line in order.order_line:
                if line.discount > order.user_id.employee_id.discount_limit:
                    self._request_discount_approval(line)

    def _request_discount_approval(self, line):
        employee = self.user_id.employee_id
        while employee and employee.approval_manager_id:
            if line.discount <= employee.approval_manager_id.discount_limit:
                self.write({'discount_approval_status': 'approved'})
                self.env['sale.order.approval.history'].create({
                    'order_id': self.id,
                    'employee_id': employee.approval_manager_id.id,
                    'status': 'approved'
                })
                self._send_approval_email(employee.approval_manager_id, self)
                return
            employee = employee.approval_manager_id

        self.write({'discount_approval_status': 'rejected'})
        raise exceptions.ValidationError("No approval manager can approve this discount.")

    def _send_approval_email(self, manager, order):
        template = self.env.ref('sale.email_template_edi_sale')
        template.send_mail(order.id, force_send=True)

    def action_confirm(self):
        if self.discount_approval_status != 'approved':
            raise exceptions.UserError("Cannot confirm order without discount approval.")
        return super(SaleOrder, self).action_confirm()

class SaleOrderApprovalHistory(models.Model):
    _name = 'sale.order.approval.history'
    _description = 'Approval History for Discounts'

    order_id = fields.Many2one('sale.order', string="Sale Order")
    employee_id = fields.Many2one('hr.employee', string="Approving Employee")
    status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Approval Status")
