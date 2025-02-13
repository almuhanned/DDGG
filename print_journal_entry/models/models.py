# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class print_journal_entery(models.Model):
#     _name = 'print_journal_entery.print_journal_entery'
#     _description = 'print_journal_entery.print_journal_entery'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
