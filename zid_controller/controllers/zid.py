import logging
import requests

from odoo import http
from werkzeug.utils import redirect

_logger = logging.getLogger(__name__)


class ZiControllers(http.Controller):
    @http.route("/zid/redirect/", methods=["GET", "POST"], auth="public", type="http")
    def zid_redirect(self):
        client_id = 1276
        base_url = "http://bashcloudmachine.xyz"
        redirect_uri = f"{base_url}/zid/callback"
        zid_url = "https://oauth.zid.sa/oauth/authorize"
        url = f"{zid_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        return redirect(url)

    @http.route("/zid/callback/", methods=["GET", "POST"], auth="public", type="http")
    def zid_callback(self, code):
        base_url = "http://bashcloudmachine.xyz"
        client_id = 1276
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": "aBYVp8ulsB2sTRX1mR5RGNBuOH4cOS6ipzqFFdMp",
            "redirect_uri": f"{base_url}/zid/callback",
            "code": code,
        }
        url = "https://oauth.zid.sa/oauth/token"
        response = requests.post(url, data=data)

        url = "https://api.zid.sa/v1/managers/account/profile"
        auth_response_json = response.json()
        payload = {}
        headers = {
            "Accept-Language": "ar",
            "Authorization": f"Bearer {auth_response_json['authorization']}",
            "Content-Type": "application/json",
            "User-Agent": "",
            "X-MANAGER-TOKEN": f"{auth_response_json['access_token']}",
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response_json = response.json()
        _logger.info(auth_response_json)
        _logger.info(response)
        _logger.info(response_json)
        _logger.info(data)
        _logger.info(response.content)
        return redirect("https://web.zid.sa/market/")
