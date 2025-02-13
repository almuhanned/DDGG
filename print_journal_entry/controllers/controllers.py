# -*- coding: utf-8 -*-
# from odoo import http


# class PrintJournalEntery(http.Controller):
#     @http.route('/print_journal_entery/print_journal_entery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/print_journal_entery/print_journal_entery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('print_journal_entery.listing', {
#             'root': '/print_journal_entery/print_journal_entery',
#             'objects': http.request.env['print_journal_entery.print_journal_entery'].search([]),
#         })

#     @http.route('/print_journal_entery/print_journal_entery/objects/<model("print_journal_entery.print_journal_entery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('print_journal_entery.object', {
#             'object': obj
#         })
