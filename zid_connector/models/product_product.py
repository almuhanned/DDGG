from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    zid_store_id = fields.Char("ZID Store ID")
    current_image_zid_id = fields.Char("Current Image ID In Zid Store")
    grand_category_id = fields.Many2one(
        "product.category", compute="_compute_grand_category_id", store=1
    )

    @api.depends("categ_id", "categ_id.parent_id")
    def _compute_grand_category_id(self):
        for rec in self:
            grand_category_id = rec.categ_id
            while grand_category_id.parent_id:
                grand_category_id = grand_category_id.parent_id
            rec.grand_category_id = grand_category_id.id
