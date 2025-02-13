import requests
import base64
from io import BytesIO
import json
from PIL import Image

from odoo import models, fields


ZID_PATHS = {
    "profile": "/managers/account/profile",
    "product": "/products/",
    "order": "/managers/store/orders",
    "category": "/managers/store/categories",
    "product_category": "/managers/store/categories",
    "category_product": "/products/",
    "payment_method": "/managers/store/payment-methods",
}


class ProductTemplate(models.Model):
    _inherit = "product.template"

    store_zid_sync_id = fields.Many2one("zid.integration")

    def action_sync_products(self):
        if self.store_zid_sync_id:

            url = self.store_zid_sync_id.clean_base_url() + ZID_PATHS["product"]

            headers = self.store_zid_sync_id.get_headers()

            to_patch_products = []
            for product in self.product_variant_ids:

                payload = {
                    "cost": round(product.standard_price, 2),
                    "sku": product.default_code or None,
                    "name": {
                        "ar": product.with_context(lang="ar_001").description_sale
                        or "",
                        "en": product.with_context(lang="en_US").description_sale or "",
                    },
                    "description": {
                        "ar": product.name or "",
                        "en": product.name or "",
                    },
                    "price": round(
                        product.product_tmpl_id._get_combination_info(
                            pricelist=self.store_zid_sync_id.pricelist_id
                        )["price"],
                        2,
                    ),
                    "is_published": True,
                }

                if not product.zid_store_id:
                    payload = json.dumps(payload)
                    response = requests.request(
                        "POST", url, headers=headers, data=payload
                    )
                    if 300 > response.status_code >= 200:
                        product.write({"zid_store_id": response.json()["id"]})
                else:
                    payload.update({"id": product.zid_store_id})
                    to_patch_products.append(payload)

                categ_id = product.grand_category_id

                if categ_id.zid_store_id:
                    payload = json.dumps({"id": categ_id.zid_store_id})
                    add_category_url = (
                        self.store_zid_sync_id.clean_base_url()
                        + f"/products/{product.zid_store_id}/categories/"
                    )
                    requests.request(
                        "POST", add_category_url, headers=headers, data=payload
                    )

            if len(to_patch_products) > 0:
                payload = json.dumps(to_patch_products)
                requests.request("PATCH", url, headers=headers, data=payload)

    def action_sync_product_price(self):
        if self.store_zid_sync_id:

            url = self.store_zid_sync_id.clean_base_url() + ZID_PATHS["product"]
            headers = self.store_zid_sync_id.get_headers()
            price_patch = []

            for product in self.product_variant_ids:
                price_patch.append(
                    {
                        "id": product.zid_store_id,
                        "price": round(
                            product.product_tmpl_id._get_combination_info(
                                pricelist=self.store_zid_sync_id.pricelist_id
                            )["price"],
                            2,
                        ),
                    }
                )

            if len(price_patch) > 0:
                payload = json.dumps(price_patch)
                requests.request("PATCH", url, headers=headers, data=payload)

    def action_sync_inventory(self):
        if self.store_zid_sync_id:

            url = self.store_zid_sync_id.clean_base_url() + ZID_PATHS["product"]
            headers = self.store_zid_sync_id.get_headers()
            inventory_patch = []

            for product in self.product_variant_ids:
                res = product.with_context(
                    location=self.store_zid_sync_id.stock_location_id.id
                )._compute_quantities_dict(None, None, None)
                inventory_patch.append(
                    {
                        "id": product.zid_store_id,
                        "quantity": res[product.id]["qty_available"],
                    }
                )

            if len(inventory_patch) > 0:
                payload = json.dumps(inventory_patch)
                requests.request("PATCH", url, headers=headers, data=payload)

    def action_sync_product_images(self):
        """Synchronize product images"""
        if self.store_zid_sync_id:

            base_url = self.store_zid_sync_id.clean_base_url() + ZID_PATHS["product"]
            headers_json = self.store_zid_sync_id.get_headers()
            headers_http = self.store_zid_sync_id.get_headers_form_data()
            payload = {"alt_text": "Image"}
            for product in self.product_variant_ids:
                if product.image_1920:
                    if product.current_image_zid_id:
                        # Delete existing product image
                        img_id_zid = product.current_image_zid_id
                        dl = f"{base_url}{product.zid_store_id}/images/{img_id_zid}/"
                        requests.request("DELETE", dl, headers=headers_json)

                    # Upload the new image
                    image = base64.b64decode(product.image_1920)
                    image = BytesIO(image)
                    image_file = Image.open(image)
                    files = [
                        (
                            "image",
                            (
                                "productimage.png",
                                image.getvalue(),
                                Image.MIME[image_file.format],
                            ),
                        )
                    ]

                    url = f"{base_url}{product.zid_store_id}/images/"
                    response = requests.request(
                        "POST", url, headers=headers_http, data=payload, files=files
                    )
                    if 300 > response.status_code >= 200:
                        # Set the id of the zid image in product
                        product.write({"current_image_zid_id": response.json()["id"]})
