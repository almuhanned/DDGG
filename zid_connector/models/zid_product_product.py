from odoo import models, fields


class ZidProductProduct(models.Model):
    _name = "zid.product.product"
    _rec_name = "odoo_product_id"

    odoo_product_id = fields.Many2one(
        comodel_name="product.product", string="Odoo Product"
    )
    zid_integration_id = fields.Many2one(
        comodel_name="zid.integration", string="ZID Integration ID", required=True
    )
