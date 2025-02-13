from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Employee(models.Model):
    _inherit = "hr.employee"

    max_discount = fields.Float(string="Maximum Discount", help="Maximum discount percentage an employee can offer without approval.")
    approval_manager = fields.Many2one('hr.employee', string="Approval Manager", help="The employee responsible for approving excess discounts.")

class SaleOrder(models.Model):
    _inherit = "sale.order"

    discount_approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string="Discount Approval Status", default='draft')

    approval_history = fields.Text(string="Approval History")

    def check_discount_approval(self):
        for order in self:
            for line in order.order_line:
                if line.discount > order.user_id.employee_id.max_discount:
                    self._request_approval(order.user_id.employee_id, line.discount)

    def _request_approval(self, employee, requested_discount):
        current_manager = employee.approval_manager
        while current_manager:
            if requested_discount <= current_manager.max_discount:
                self.write({
                    'discount_approval_state': 'approved',
                    'approval_history': (self.approval_history or "") + f"\nApproved by {current_manager.name}"
                })
                return
            self._send_approval_notification(current_manager, requested_discount)
            current_manager = current_manager.approval_manager

        self.write({
            'discount_approval_state': 'rejected',
            'approval_history': (self.approval_history or "") + "\nDiscount request rejected: No manager can approve."
        })
        raise ValidationError("Discount request denied: No manager can approve this discount.")

    def _send_approval_notification(self, manager, discount):
        mail_template = self.env.ref('mail.template_discount_approval_request', raise_if_not_found=False)
        if mail_template:
            mail_template.sudo().send_mail(manager.user_id.id, force_send=True)

    @api.constrains('order_line')
    def prevent_processing_before_approval(self):
        for order in self:
            if order.discount_approval_state in ['pending', 'rejected']:
                raise ValidationError("Cannot generate invoice or delivery order until the discount is approved.")

    def action_confirm(self):
        if self.discount_approval_state != 'approved':
            raise ValidationError("Discount must be approved before confirming the order.")
        return super(SaleOrder, self).action_confirm()
