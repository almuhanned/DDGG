# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError



class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Res partner Sequences"

    _sql_constraints = [
        ('ref_uniq', 'unique (ref)', 'The sequence must be unique !')
    ]
    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('res.partner') or '/'
        return super(ResPartner, self).create(vals)

    @api.constrains('ref')
    def _check_ref_unique(self):
        ref_counts = self.env['res.partner'].search_count([('ref', '=', self.ref)])
        print(ref_counts)
        if ref_counts > 1 and self.ref:
            raise ValidationError("Sequence number already exists!")

    # @api.model
    # def write(self, vals):
    #     ref_exist = self.env['res.partner'].search(
    #         [('ref', '=', self.ref)])
    #     print('##################################################',ref_exist)
    #     if len(ref_exist) > 1:
    #         raise ValidationError(_("The employee has already a pending installment"))
    #     return super(ResPartner, self).write(vals)

