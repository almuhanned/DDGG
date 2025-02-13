#-*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale(models.Model):
    _inherit = "sale.order"
    
    create_user = fields.Many2one("res.users",compute='_compute_create_user')

    def _compute_create_user(self):
        for res in self:
            res.create_user = res.create_uid