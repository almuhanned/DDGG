import json
import logging

from odoo import http
from odoo.http import request
from .utils import URL_PREFIX, valid_response

_logger = logging.getLogger(__name__)

STATUS_METHOD_MAPPING = {
    "new": "process_new()",
    "ready": "process_ready()",
    "indelivery": "process_indelivery()",
    "delivered": "process_delivered()",
    "reversed": "process_reversed()",
    "canceled": "process_canceled()",
}


class ZidAPI(http.Controller):
    @http.route(
        [URL_PREFIX + "/zid/create_order"],
        methods=["POST"],
        type="json",
        auth="public",
        csrf=False,
        sitemap=False,
    )
    def create_order(self, **payload):
        payload = json.loads(request.httprequest.data.decode())
        _logger.info(payload)
        store = (
            request.env["zid.store"]
            .sudo()
            .search([("store_id", "=", payload["store_id"])], limit=1)
        )
        order_id = (
            request.env["sale.order"]
            .sudo()
            .create_order_from_payload(store, payload)
        )
        # if payload["order_status"]["code"] in STATUS_METHOD_MAPPING:
        #     eval("order_id." + STATUS_METHOD_MAPPING[payload["order_status"]["code"]])
        return valid_response({}, 200)

    @http.route(
        [URL_PREFIX + "/zid/update_order"],
        methods=["POST"],
        type="json",
        auth="public",
        csrf=False,
        sitemap=False,
    )
    def update_order(self, **payload):
        payload = json.loads(request.httprequest.data.decode())
        _logger.info(payload)
        if payload["order_status"]["code"] in STATUS_METHOD_MAPPING:
            sale_order = (
                request.env["sale.order"]
                .sudo()
                .search([("id_in_zid_store", "=", str(payload["id"]))])
            )
            eval("sale_order." + STATUS_METHOD_MAPPING[payload["order_status"]["code"]])
        return valid_response({}, 200)
