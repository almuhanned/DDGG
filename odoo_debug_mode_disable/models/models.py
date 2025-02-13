# -*- coding: utf-8 -*-

import werkzeug.exceptions

from odoo import models, api
from odoo.http import request


class View(models.Model):
    _inherit = 'ir.ui.view'


    @api.model
    def _prepare_qcontext(self):
        qcontext = super(View, self)._prepare_qcontext()
        # print("qcontext", qcontext)
        if qcontext.get("debug"):
            user_id = qcontext.get("user_id")
            if not user_id.has_group('odoo_debug_mode_disable.group_access_debug_mode'):
                qcontext.update(debug="")
        return qcontext


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _dispatch(cls):
        res = super(IrHttp, cls)._dispatch()
        if request.session.uid:
            user = request.env["res.users"].browse(request.session.uid)
            if not user.has_group('odoo_debug_mode_disable.group_access_debug_mode'):
                request.session.debug = ""
        return res
