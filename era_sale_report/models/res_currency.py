from odoo import api, fields, models

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    full_name = fields.Char(string='Name', translate=True)

