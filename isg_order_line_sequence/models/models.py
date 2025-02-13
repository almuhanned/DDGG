from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
   
    @api.model
    def create(self, values):
        if 'order_id' in values:
            order_id = values.get('order_id')
            last_line = self.env['sale.order.line'].search([('order_id', '=', order_id)], order='sequence desc', limit=1)
            last_sequence = last_line.sequence if last_line else 0
            values['sequence'] = last_sequence + 1

        return super(SaleOrderLine, self).create(values)
