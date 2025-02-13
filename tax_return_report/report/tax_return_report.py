# -*- coding: utf-8 -*-

from odoo import models,api,fields,_


class TaxReturnAbstract(models.AbstractModel):
    _name = 'report.tax_return_report.report_tax_return_report'

    
    @api.model
    def _get_report_values(self, docids, data=None):
        final_list = []
        for record in data['docs']:
            line_id = self.env['account.move.line'].search([('id','=',record[7])])
            record_dict = {'line' : line_id}
            final_list.append(record_dict)


        return {
                'docs': final_list,
                'currency_id' : self.env.company.currency_id.id,
                'start_date': data['start_date'],
                'end_date': data['end_date']
            }
    