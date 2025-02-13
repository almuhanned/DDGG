# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_in_text = fields.Text(string='Text', compute="_compute_total_in_text")
    inv_sale_id = fields.Many2one("sale.order",compute='_compute_inv_sale_id_loc')
    location_id = fields.Many2one("stock.location",compute='_compute_inv_sale_id_loc')
    create_user = fields.Many2one("res.users",compute='_compute_create_user')

    def _compute_total_in_text(self):
        for rec in self:
            total_in_text = num2words(rec.amount_total, lang='ar')
            rec.total_in_text = total_in_text


    def _compute_inv_sale_id_loc(self):
        for move in self:
            move.inv_sale_id = self.env['sale.order'].search([('name','=',move.invoice_origin)],limit=1).id
            move.location_id = False
            
            if move.inv_sale_id:
                picking = self.env['stock.picking'].search([('origin','=',move.inv_sale_id.name)],limit=1)
                
                if picking:
                    location_id = picking.id


    def _compute_create_user(self):
        for res in self:
            res.create_user = res.create_uid
