# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import timedelta, datetime, date
from dateutil import relativedelta

class HREmployee(models.Model):
    _inherit = 'hr.employee'

    rejoin_period = fields.Char(string='Rejoin Period', compute='compute_rejoin_date_period')
    
    @api.depends('rejoin_date')
    def compute_rejoin_date_period(self):
        for rec in self:
            if rec.rejoin_date:
                rec.rejoin_period = " "
                rejoin_date = rec.rejoin_date
                today_date = fields.date.today()
                start_date = datetime.strptime(str(rejoin_date), "%Y-%m-%d")
                end_date = datetime.strptime(str(today_date), "%Y-%m-%d")
                delta = relativedelta.relativedelta(end_date, start_date)
                if delta:
                    rec.rejoin_period = str(delta.years) + " " + 'Years,' + \
                                                      str(delta.months) + " " + 'months,' + \
                                                      " " + str(delta.days) + " " + 'days'
            else:
                rec.rejoin_period = " "
    
    