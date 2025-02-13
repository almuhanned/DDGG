import logging
import json

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ZiControllers(http.Controller):
    @http.route("/zid/webhook/", methods=["POST"], auth="public", type="json")
    def zid_redirect(self):
        payload = request.httprequest.data.decode()
        payload = json.loads(payload)
        _logger.info(payload)
