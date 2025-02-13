# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _

class account_payment(models.Model):
    _inherit = "account.payment"

    @api.depends('amount')
    def _compute_amount_in_word(self):
        for rec in self:
            if rec.currency_id:
                rec.custom_amount_in_word = rec.currency_id.amount_to_text(rec.amount)    

    is_show_amount_in_word = fields.Boolean(
        string="Show Word Amount Report?",
        default=True,
        copy=True
    )
    custom_amount_in_word = fields.Char(
        string="Total Amount In Word",
        compute='_compute_amount_in_word',
    )