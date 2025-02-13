from odoo import api, fields, models

class ApprovalTracking(models.Model):
    _name = 'approval.tracking'
    _rec_name = 'name'
    _description = 'Approval Tracking'

    name = fields.Char(translate=True)
    user_id = fields.Many2one('res.users', string='User')
    date = fields.Date(string="Date", default=fields.Date.today)
    purchase_id = fields.Many2one('purchase.order', string='Purchase')
    digital_signature = fields.Binary(string="Signature", related='user_id.digital_signature')

