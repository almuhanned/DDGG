# -*- coding : utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ResCompany(models.Model):
    _inherit = "res.company"

    allow_out_of_contract_weekend = fields.Boolean(string="Allow Out of Contract Weekend", default=True)
