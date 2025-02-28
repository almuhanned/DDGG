# Copyright 2016-TODAY Serpent Consulting Services Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo.tests import common


class PurchaseReportProductImageTestCase(common.TransactionCase):

    def setup(self):
        super(PurchaseReportProductImageTestCase, self).setup()

    def test_purchase_report_product(self):
        self.product = self.env.ref("product.product_product_7")
        self.partner = self.env.ref("base.res_partner_2")

        self.purchase_order = self.env["purchase.order"].create(
            {
                "partner_id": self.partner.id,
                "partner_invoice_id": self.partner.id,
                "partner_shipping_id": self.partner.id,
                "pricelist_id": self.env.ref("product.list0").id,
                "print_image": "True",
                "image_sizes": "image_medium",
            }
        )
        self.purchase_order_line = self.env["purchase.order.line"].create(
            {
                "name": self.product and self.product.name or " ",
                "product_id": self.product and self.product.id or False,
                "product_uom_qty": 2,
                "product_uom": self.product.uom_id.id,
                "price_unit": self.product.list_price,
                "order_id": self.sale_order.id,
                "tax_id": False,
                "image_small": self.product.image_1920,
            }
        )
