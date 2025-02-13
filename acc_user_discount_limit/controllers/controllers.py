# -*- coding: utf-8 -*-
# from odoo import http


# class AccUserDiscountLimit(http.Controller):
#     @http.route('/acc_user_discount_limit/acc_user_discount_limit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/acc_user_discount_limit/acc_user_discount_limit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('acc_user_discount_limit.listing', {
#             'root': '/acc_user_discount_limit/acc_user_discount_limit',
#             'objects': http.request.env['acc_user_discount_limit.acc_user_discount_limit'].search([]),
#         })

#     @http.route('/acc_user_discount_limit/acc_user_discount_limit/objects/<model("acc_user_discount_limit.acc_user_discount_limit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('acc_user_discount_limit.object', {
#             'object': obj
#         })
