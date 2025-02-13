# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):

        partner_discount_limit = self.env.user.partner_id.discount_limit
        
        if self.amount_untaxed > 0:
            tot_disc_percentage = \
            (self.ks_amount_discount + self.special_discount) / self.amount_before_discount *100

            if tot_disc_percentage > partner_discount_limit:
                allowed_partner = self.env['res.partner'].search([('discount_limit','>',tot_disc_percentage)],limit=1)
                
                if allowed_partner:
                    raise ValidationError(_("Sorry, the entered discount is above your allowed limit!!\nPlease switch to %s") % (allowed_partner.name))

                else:
                    raise ValidationError(_("Sorry, the entered discount is above your allowed limit!!\nNo user found with this authority! "))

        return super(SaleOrder, self).action_confirm()
