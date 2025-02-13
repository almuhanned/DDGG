# See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    print_image = fields.Boolean("Print Image",
        help="""If ticked, you can see the product image in 
report of sale order/quotation""")
    image_sizes = fields.Selection(
        [("image", "Big sized Image"),
        ("image_medium", "Medium Sized Image"),
        ("image_small", "Small Sized Image"),
        ], "Image Sizes", default="image_small",
        help="Image size to be displayed in report")


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    image_small = fields.Binary("Product Image", related="product_id.image_1920")
