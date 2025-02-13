# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    is_stranger = fields.Boolean(string="Is not saudi", default=False)
    passport_end_date = fields.Date(string="Passport End Date",)
    iqamah_number = fields.Char(string="Iqamah NO",)
    iqamah_end_date = fields.Date(string="Iqamah End Date",)
    license_no = fields.Char(string=" Driving License NO", )
    license_end_date = fields.Date(string="Driving License End Date",)
