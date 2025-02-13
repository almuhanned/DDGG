from odoo import models, fields


class ProductCategory(models.Model):
    _inherit = "product.category"

    zid_store_id = fields.Char("ZID Store ID")
    sync_zid = fields.Boolean("Allow sync to zid store", default=True)
