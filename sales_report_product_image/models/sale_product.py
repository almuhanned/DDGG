# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    print_image = fields.Boolean("Print Image",
        help="""If ticked, you can see the product image in 
report of sale order/quotation""")
    image_sizes = fields.Selection(
        [("image", "Big sized Image"),
        ("image_medium", "Medium Sized Image"),
        ("image_small", "Small Sized Image"),
        ], "Image Sizes", default="image_small",
        help="Image size to be displayed in report")
    # @api.depends("order_line")
    # def _compute_max_line_sequence(self):
    #     """Allow to know the highest sequence entered in sale order lines.
    #     Then we add 1 to this value for the next sequence.
    #     This value is given to the context of the o2m field in the view.
    #     So when we create new sale order lines, the sequence is automatically
    #     added as :  max_sequence + 1
    #     """
    #     for sale in self:
    #         sale.max_line_sequence = max(sale.mapped("order_line.sequence") or [0]) + 1

    max_line_sequence = fields.Integer(
        string="Max sequence in lines", 
    )

    def _reset_sequence(self):
        for rec in self:
            current_sequence = 1
            for line in sorted(rec.order_line, key=lambda x: (x.sequence, x.id)):
                if line.sequence != current_sequence:
                    line.sequence = current_sequence
                current_sequence += 1

    def write(self, line_values):
        res = super(SaleOrder, self).write(line_values)
        self._reset_sequence()
        return res

    def copy(self, default=None):
        return super(SaleOrder, self.with_context(keep_line_sequence=True)).copy(
            default
        )

    def update_product_image(self):
        for order in self:
            order.order_line._onchange_product_id_image()
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    image_small = fields.Binary("Product Image")

        # re-defines the field to change the default


    sequence = fields.Integer(
        help="Gives the sequence of this line when displaying the sale order.",
        default=9999,
        string="Sequence",
    )

    @api.onchange("product_id")
    def _onchange_product_id_image(self):
        for line in self:
            if line.product_id:
                line.image_small = line.product_id.image_1920

    @api.model
    def create(self, values):
        line = super(SaleOrderLine, self).create(values)
        # We do not reset the sequence if we are copying a complete sale order
        if self.env.context.get("keep_line_sequence"):
            line.order_id._reset_sequence()
        return line
