from odoo import models, fields


class ZidPaymentMethod(models.Model):
    _name = "zid.payment.method"
    _description = "Zid Payment Method"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    zid_integration_id = fields.Many2one("zid.integration")
    zid_store_id = fields.Char("ZID Store ID")
    name = fields.Char("Name", required=1)
    code = fields.Char("Code")
    fees = fields.Float("Fees")
    journal_id = fields.Many2one("account.journal", "Journal")
    enabled = fields.Boolean("Enabled")
