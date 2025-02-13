# -*- coding: utf-8 -*-
# from odoo import http


# class TaxReturnReport(http.Controller):
#     @http.route('/tax_return_report/tax_return_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_return_report/tax_return_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_return_report.listing', {
#             'root': '/tax_return_report/tax_return_report',
#             'objects': http.request.env['tax_return_report.tax_return_report'].search([]),
#         })

#     @http.route('/tax_return_report/tax_return_report/objects/<model("tax_return_report.tax_return_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_return_report.object', {
#             'object': obj
#         })
