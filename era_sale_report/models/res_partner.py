from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    name = fields.Char(index=True, translate=True)

    @api.depends_context('company')
    def _credit_debit_get(self):
        if not self.ids:
            self.debit = False
            self.credit = False
            return
        return super(ResPartner, self)._credit_debit_get()
