# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    allow_out_of_contract_weekend = fields.Boolean(string="Allow Out of Contract Weekend", related="company_id.allow_out_of_contract_weekend", readonly=False)
