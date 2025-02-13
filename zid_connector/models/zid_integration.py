import time
import requests
import base64
from io import BytesIO
import json
from PIL import Image
from dateutil import relativedelta

from odoo import models, fields, _, api
from odoo.exceptions import UserError

ZID_PATHS = {
    "profile": "/managers/account/profile",
    "product": "/products/",
    "order": "/managers/store/orders",
    "category": "/managers/store/categories",
    "product_category": "/managers/store/categories",
    "category_product": "/products/",
    "payment_method": "/managers/store/payment-methods",
}


class ZidIntegration(models.Model):
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _name = "zid.integration"
    _description = "Zid Integration"

    # Basic configuration
    name = fields.Char("Integration Name", required=1)
    base_url = fields.Char("API URL", required=1, help="API URL")
    zid_store_id = fields.Char("Store ID", required=1)
    authorization = fields.Char("Authorization", required=1)
    refresh_token = fields.Char("Refresh Token", required=1)
    access_token = fields.Char("Access Token", required=1, help="X-Manager-Token")

    # Product sync options
    pricelist_id = fields.Many2one("product.pricelist", "Pricelist")
    stock_location_id = fields.Many2one("stock.location", "Stock Location")

    # Last sync time
    last_order_sync = fields.Datetime("Last Orders sync")
    last_product_sync = fields.Datetime("Last products sync")
    last_product_category_sync = fields.Datetime("Last product Category sync")

    # Initial product uploading
    product_export_limit = fields.Integer("Product Sync Limit", default=20)
    product_export_offset = fields.Integer("Product Sync Offset", default=0)

    # Order sync options
    default_sale_tax_id = fields.Many2one("account.tax", "Default Tax")
    default_customer_id = fields.Many2one("res.partner", "Default Customer")
    coupon_product_id = fields.Many2one("product.product", "Coupon Product")
    delivery_product_id = fields.Many2one("product.product", "Delivery Product")
    zid_cod_product_id = fields.Many2one("product.product", "ZID COD Product")
    sales_team_id = fields.Many2one("crm.team", "Sales Team")

    @api.model
    def cron_sync_products(self):
        integrations = self.search([])
        for integration in integrations:
            integration.action_sync_products()
            integration.action_sync_inventory()
            integration.action_sync_product_images()
            integration.product_export_offset += integration.product_export_limit

    def clean_base_url(self):
        self.ensure_one()
        if self.base_url[-1] == "/":
            return self.base_url[:-1]
        else:
            return self.base_url

    def get_headers(self):
        return {
            "Accept-Language": "ar",
            "Authorization": f"Bearer {self.authorization}",
            "Content-Type": "application/json",
            "ROLE": "Manager",
            "STORE-ID": self.zid_store_id,
            "X-MANAGER-TOKEN": self.access_token,
        }

    def get_headers_simple(self):
        return {
            "Accept-Language": "ar",
            "Authorization": f"Bearer {self.authorization}",
            "Content-Type": "application/json",
            "X-MANAGER-TOKEN": self.access_token,
        }

    def get_headers_form_data(self):
        return {
            "Accept-Language": "ar",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.authorization}",
            "ROLE": "Manager",
            "STORE-ID": self.zid_store_id,
            "X-MANAGER-TOKEN": self.access_token,
        }

    def action_test_connection(self):
        url = self.clean_base_url() + ZID_PATHS["profile"]
        headers = self.get_headers_simple()
        payload = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        if (
            300 > response.status_code >= 200
            and response.headers.get("Content-Type", False)
            == "application/json; charset=utf-8"
        ):
            if response.json()["status"] == "object":
                return {
                    "type": "ir.actions.client",
                    "tag": "display_notification",
                    "params": {
                        "message": _("Connection Test Successful!"),
                        "type": "success",
                        "sticky": False,
                    },
                }
            else:
                raise UserError(_("Connection test failed."))
        else:
            raise UserError(_("Connection test failed."))

    def action_sync_product_categories(self):
        domain = [
            ("write_date", ">=", self.last_product_category_sync),
            ("parent_id", "=", False),
            ("sync_zid", "=", True),
        ]
        updated_product_categories = self.env["product.category"].search(domain)
        category_url = self.clean_base_url() + ZID_PATHS["category"]
        headers = self.get_headers_form_data()
        for product_category in updated_product_categories:
            payload = {
                "name[ar]": product_category.with_context(lang="ar").name,
                "name[en]": product_category.with_context(lang="en_US").name,
                "description[ar]": product_category.with_context(lang="ar").name,
                "description[en]": product_category.with_context(lang="en_US").name,
            }
            if not product_category.zid_store_id:
                url = category_url + "/add"
                response = requests.request("POST", url, headers=headers, data=payload)
                if 300 > response.status_code >= 200:
                    product_category.write(
                        {"zid_store_id": response.json()["category"]["id"]}
                    )
            else:
                url = category_url + f"/{product_category.zid_store_id}/update"
                response = requests.request("POST", url, headers=headers, data=payload)
            time.sleep(1)

    def action_sync_products(self):
        domain = [
            ("sale_ok", "=", True),
            ("product_tmpl_id.image_1920", "!=", False),
            ("product_tmpl_id.qty_available", ">", 0),
            ("default_code", "!=", False),
            ("grand_category_id.sync_zid", "=", True),
            "|",
            ("write_date", ">=", self.last_product_sync),
            ("product_tmpl_id.write_date", ">=", self.last_product_sync),
        ]
        updated_products = self.env["product.product"].search(
            domain, limit=self.product_export_limit, offset=self.product_export_offset
        )

        url = self.clean_base_url() + ZID_PATHS["product"]

        headers = self.get_headers()

        to_patch_products = []

        for product in updated_products:
            payload = {
                "cost": round(product.standard_price, 2),
                "sku": product.default_code or None,
                "name": {
                    "ar": product.with_context(lang="ar_001").description_sale or "",
                    "en": product.with_context(lang="en_US").description_sale or "",
                },
                "description": {
                    "ar": product.name or "",
                    "en": product.name or "",
                },
                "price": round(
                    product.product_tmpl_id._get_combination_info(
                        pricelist=self.pricelist_id
                    )["price"],
                    2,
                ),
                "is_published": True,
            }

            if not product.zid_store_id:
                payload = json.dumps(payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                if 300 > response.status_code >= 200:
                    product.write({"zid_store_id": response.json()["id"]})
            else:
                payload.update({"id": product.zid_store_id})
                to_patch_products.append(payload)

            categ_id = product.grand_category_id

            if categ_id.zid_store_id:
                payload = json.dumps({"id": categ_id.zid_store_id})
                add_category_url = (
                    self.clean_base_url()
                    + f"/products/{product.zid_store_id}/categories/"
                )
                requests.request(
                    "POST", add_category_url, headers=headers, data=payload
                )
            time.sleep(1)

        if len(to_patch_products) > 0:
            payload = json.dumps(to_patch_products)
            requests.request("PATCH", url, headers=headers, data=payload)

    def action_sync_inventory(self):
        domain = [
            ("sale_ok", "=", True),
            ("product_tmpl_id.image_1920", "!=", False),
            ("detailed_type", "=", "product"),
            ("default_code", "!=", False),
            ("zid_store_id", "!=", False),
        ]
        products = self.env["product.product"].search(
            domain, limit=self.product_export_limit, offset=self.product_export_offset
        )
        url = self.clean_base_url() + ZID_PATHS["product"]
        headers = self.get_headers()
        inventory_patch = []
        for product in products:
            res = product.with_context(
                location=self.stock_location_id.id
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
        time.sleep(1)

    def action_sync_product_images(self):
        """Synchronize product images"""
        domain = [
            ("sale_ok", "=", True),
            ("product_tmpl_id.image_1920", "!=", False),
            ("default_code", "!=", False),
            ("zid_store_id", "!=", False),
        ]
        products = self.env["product.product"].search(
            domain, limit=self.product_export_limit, offset=self.product_export_offset
        )
        base_url = self.clean_base_url() + ZID_PATHS["product"]
        headers_json = self.get_headers()
        headers_http = self.get_headers_form_data()
        payload = {"alt_text": "Image"}
        for product in products:
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
                time.sleep(1)

    def action_sync_payment_methods(self):
        """_summary_"""
        url = self.clean_base_url() + ZID_PATHS["payment_method"]
        headers = self.get_headers()
        response = requests.get(url, data={}, headers=headers)
        cr = self.env.cr
        if 200 <= response.status_code < 300 and "payload" in response.json():
            sql = "SELECT id FROM zid_payment_method WHERE zid_store_id = %s"
            for payment_method in response.json()["payload"]:
                cr.execute(sql, (str(payment_method["id"]),))
                payment_methods = cr.dictfetchall()
                if len(payment_methods) == 0:
                    self.env["zid.payment.method"].create(
                        {
                            "name": payment_method["name"],
                            "code": str(payment_method["code"]),
                            "fees": payment_method["fees"],
                            "enabled": payment_method["enabled"],
                            "zid_store_id": str(payment_method["id"]),
                            "zid_integration_id": self.id,
                        }
                    )
                else:
                    self.env["zid.payment.method"].browse(
                        payment_methods[0]["id"]
                    ).write(
                        {
                            "name": payment_method["name"],
                            "code": str(payment_method["code"]),
                            "fees": payment_method["fees"],
                            "enabled": payment_method["enabled"],
                        }
                    )

    @api.model
    def cron_sync_orders(self):
        integrations = self.search([])
        for integration in integrations:
            integration.action_sync_orders()

    def action_sync_orders(self):
        filter_date = self.last_order_sync or fields.Date.today()
        filter_date = filter_date - relativedelta.relativedelta(days=1)
        last_sync = filter_date.strftime("%Y-%m-%d")

        url = self.clean_base_url() + ZID_PATHS["order"]
        headers = self.get_headers()
        payload = {}
        statuses = ["new", "preparing", "ready", "indelivery", "delivered"]
        for status in statuses:
            page = 0
            while True:
                page += 1
                date_from_str = last_sync
                date_to_str = fields.date.today().strftime("%Y-%m-%d")
                page_url = (
                    f"{url}?payload_type=print&page={page}&per_page=10"
                    f"&date_from={date_from_str}&date_to={date_to_str}"
                    f"&order_status={status}"
                )
                response = requests.get(page_url, data=payload, headers=headers)
                cr = self.env.cr
                if (
                    200 <= response.status_code < 300
                    and "orders" in response.json()
                    and len(response.json()["orders"]) > 0
                ):
                    sql = "SELECT id FROM sale_order WHERE zid_store_id = %s"
                    for order in response.json()["orders"]:
                        cr.execute(sql, (str(order["id"]),))
                        orders = cr.dictfetchall()
                        if len(orders) == 0:
                            self.env["sale.order"].sudo().create_order_from_payload(
                                self, order
                            )
                else:
                    break
                # Commit submitted orders
                self.env.cr.commit()

        self.last_order_sync = fields.Date.today()
