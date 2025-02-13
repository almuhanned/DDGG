from odoo import api, fields, models


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    project_name = fields.Char(string="Project")

