# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
#
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    logo2 = fields.Binary('Secound Logo', readonly=False)


class BaseDocumentLayout(models.TransientModel):

    _inherit = 'base.document.layout'

    logo2 = fields.Binary(related='company_id.logo2', readonly=False)
