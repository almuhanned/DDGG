# -*- coding: utf-8 -*-


from odoo import models, fields, api, tools, _
import babel
import time
from datetime import datetime, timedelta


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Employee'

    latee = fields.Integer(string="latee")
    early_leave = fields.Integer(string="early leave")
    days_latee = fields.Integer(string="days latee")

