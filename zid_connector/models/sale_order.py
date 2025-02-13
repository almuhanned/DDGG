from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    zid_payment_method_id = fields.Many2one("zid.payment.method", "Zid Payment Method")
    zid_store_id = fields.Char("ZID Store ID", index=True)
    zid_integration_id = fields.Many2one("zid.integration")

    @api.model
    def create_order_from_payload(self, store, order):
        cr = self.env.cr
        customer_id = store.default_customer_id
        lines = []
        for product in order["products"]:
            product_sql = (
                "SELECT id FROM product_product WHERE default_code = %s limit 1"
            )
            cr.execute(product_sql, (product["sku"],))
            product_id = cr.fetchone()
            if product_id is not None:
                lines.append(
                    [
                        0,
                        0,
                        {
                            "product_id": product_id[0],
                            "product_uom_qty": product["quantity"],
                            "price_unit": product["price"],
                            "tax_id": [],
                        },
                    ]
                )
                if product["is_taxable"]:
                    lines[-1][2]["tax_id"] = (
                        [store.default_sale_tax_id.id]
                        if store.default_sale_tax_id
                        else []
                    )
            else:
                continue

        # Coupon product
        if len([x for x in order["payment"]["invoice"] if x["code"] == "coupon"]) > 0:
            price = -(
                float(
                    [x for x in order["payment"]["invoice"] if x["code"] == "coupon"][
                        0
                    ]["value"]
                )
            )
            lines.append(
                [
                    0,
                    0,
                    {
                        "product_id": store.coupon_product_id.id,
                        "product_uom_qty": 1,
                        "price_unit": -price,
                    },
                ]
            )

        # Shipping product
        if len([x for x in order["payment"]["invoice"] if x["code"] == "shipping"]) > 0:
            lines.append(
                [
                    0,
                    0,
                    {
                        "product_id": store.delivery_product_id.id,
                        "product_uom_qty": 1,
                        "price_unit": float(
                            [
                                x
                                for x in order["payment"]["invoice"]
                                if x["code"] == "shipping"
                            ][0]["value"]
                        ),
                    },
                ]
            )

        # Cash on delivery product
        if len([x for x in order["payment"]["invoice"] if x["code"] == "zid_cod"]) > 0:
            lines.append(
                [
                    0,
                    0,
                    {
                        "product_id": store.zid_cod_product_id.id,
                        "product_uom_qty": 1,
                        "price_unit": float(
                            [
                                x
                                for x in order["payment"]["invoice"]
                                if x["code"] == "zid_cod"
                            ][0]["value"]
                        ),
                    },
                ]
            )

        so_vals = {
            "partner_id": customer_id.id,
            "zid_store_id": order["id"],
            "zid_integration_id": store.id,
            "team_id": store.sales_team_id.id,
            "date_order": order["created_at"],
            "order_line": lines,
        }

        # Payment method
        if (
            "payment" in order
            and "method" in order["payment"]
            and order["payment"]["method"] is not None
        ):
            code = order["payment"]["method"]
            payment_method = (
                store.env["zid.payment.method"]
                .sudo()
                .search([("code", "=", code)], limit=1)
            )
            if payment_method:
                so_vals.update(
                    {
                        "zid_payment_method_id": payment_method.id,
                    }
                )

        sale_order = store.env["sale.order"].create(so_vals)

        # if sale_order:
        #     sale_order.action_confirm()
        #     try:
        #         for picking in sale_order.picking_ids:
        #             picking.action_assign()
        #             picking.action_set_quantities_to_reservation()
        #             picking.action_confirm()
        #             picking.button_validate()
        #     except Exception:
        #         print("ERROR DELIVERY")

        #     try:
        #         sale_order._create_invoices()
        #     except Exception:
        #         print("Invoice Creation Exception")

        #     if len(sale_order.invoice_ids) > 0:
        #         for invoice in sale_order.invoice_ids.sudo():
        #             invoice.action_post()
        #             invoice.with_context(
        #                 check_move_validity=False
        #             )._recompute_dynamic_lines(
        #                 recompute_all_taxes=True, recompute_tax_base_amount=True
        #             )
        #         if sale_order.zid_payment_method_id.journal_id:
        #             journal_id = sale_order.zid_payment_method_id.journal_id
        #             register_payment = (
        #                 store.env["account.payment.register"]
        #                 .sudo()
        #                 .with_context(
        #                     active_model="account.move",
        #                     active_ids=sale_order.invoice_ids.ids,
        #                 )
        #                 .create(
        #                     {
        #                         "journal_id": journal_id.id,
        #                     }
        #                 )
        #             )
        #             register_payment._create_payments()
