# -*- coding: utf-8 -*-
# from odoo import http


# class DiscountCustom(http.Controller):
#     @http.route('/discount_custom/discount_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/discount_custom/discount_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('discount_custom.listing', {
#             'root': '/discount_custom/discount_custom',
#             'objects': http.request.env['discount_custom.discount_custom'].search([]),
#         })

#     @http.route('/discount_custom/discount_custom/objects/<model("discount_custom.discount_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('discount_custom.object', {
#             'object': obj
#         })
