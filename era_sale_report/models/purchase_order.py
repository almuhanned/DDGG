from odoo import api, fields, models, _


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    contact_person = fields.Char(string="Contact Person")
    contact_phone = fields.Char(string="Phone")
    contact_email = fields.Char(string="Email")

    payment_method_id = fields.Many2one(comodel_name="payment.method", string="Payment Method")
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchasing', 'Purchasing'),
        ('accounting', 'Accounting'),
        ('general_manager', 'General Manager'),
        ('ceo', 'CEO Manager'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)
    approval_tracking_ids = fields.One2many(comodel_name="approval.tracking", inverse_name="purchase_id", string="Approval Tracking")


    def send_request(self):
        for order in self:
            order.state = 'purchasing'
    def purchasing_approve(self):
        for order in self:
            order.approval_tracking_ids = [(0, 0, {'name': _('Purchasing'), 'user_id': self.env.user.id})]
            order.state = 'accounting'

    def accounting_approve(self):
        for order in self:
            order.approval_tracking_ids = [(0, 0, {'name': _('Accounting'), 'user_id': self.env.user.id})]
            order.state = 'general_manager'

    def general_manager_approve(self):
        for order in self:
            order.approval_tracking_ids = [(0, 0, {'name': _('General Manager'), 'user_id': self.env.user.id})]
            order.state = 'ceo'


    def button_confirm(self):
        for order in self:
            if order.state not in ['ceo']:
                continue
            order._add_supplier_to_product()
            # Deal with double validation process
            if order._approval_allowed():
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
            order.approval_tracking_ids = [(0, 0, {'name': _('CEO Manager'), 'user_id': self.env.user.id})]
        return True

    def button_draft(self):
        res = super(PurchaseOrderInherit, self).button_draft()
        self.approval_tracking_ids = [(5, 0, 0)]
        return res


class PaymentMethod(models.Model):
    _name = 'payment.method'
    _rec_name = 'name'
    _description = 'Payment Method'

    name = fields.Char(required=True)

