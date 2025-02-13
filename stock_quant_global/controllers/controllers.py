# -*- coding: utf-8 -*-
# from odoo import http


# class ProductQuantity(http.Controller):
#     @http.route('/product_quantity/product_quantity/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_quantity/product_quantity/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_quantity.listing', {
#             'root': '/product_quantity/product_quantity',
#             'objects': http.request.env['product_quantity.product_quantity'].search([]),
#         })

#     @http.route('/product_quantity/product_quantity/objects/<model("product_quantity.product_quantity"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_quantity.object', {
#             'object': obj
#         })
