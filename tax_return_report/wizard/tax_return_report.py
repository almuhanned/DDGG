# -*- coding: utf-8 -*-

import io
import xlsxwriter
import base64

from odoo import models, fields, api, _


class PartnerLedgerWizard(models.TransientModel):
    _name = "tax.return.report"
    _description = "Tax return report"

    start_date = fields.Date(string="Start Date",required=True)
    end_date = fields.Date(string="End Date",required=True)
    report_type = fields.Selection([
        ('excel', 'Excel'),
        ('pdf', 'PDF'),
    ], string="Report Type", required=True,default='excel')
    

    def get_taxed_lines(self):
        query = """
            select sml.price_subtotal,sml.l10n_gcc_invoice_tax_amount,sml.price_total,sml.partner_id,sml.invoice_no ,
                 sml.name,sml.date,sml.id from 
                account_move sm inner join account_move_line sml on sm.id = sml.move_id INNER JOIN 
                account_move_line_account_tax_rel AS move_tax ON sml.id = move_tax.account_move_line_id inner join 
                account_tax tax on move_tax.account_tax_id = tax.id 
                AND sm.date > %s
                AND sm.date <= %s
        """
        self.env.cr.execute(query, (self.start_date, self.end_date))
        return self._cr.fetchall()

    def get_report(self):
        result = self.get_taxed_lines()
        if self.report_type == 'excel':
            output = io.BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            sheet = workbook.add_worksheet()
            head = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 10})
            title_style = workbook.add_format(
            {'font_name': 'Arial', 'bold': True,'bg_color': 'white','font_size': 10, 'font_color': 'black',
             'align': 'left', 'border': False})
            title_style2 = workbook.add_format(
            {'font_name': 'Arial', 'bold': True,'bg_color': 'white','font_size': 10, 'font_color': 'black',
             'align': 'center','bottom': 30, 'border': False})
            title_style3 = workbook.add_format(
            {'font_name': 'Arial', 'bold': True,'bg_color': 'white','font_size': 10, 'font_color': 'black',
             'align': 'right','bottom': 30, 'border': False})
            title_style4 = workbook.add_format(
            {'font_name': 'Arial','font_size': 14, 'font_color': 'black',
             'align': 'center','bottom': 30, 'color': 'red','border':2, 'valign': 'vcenter', 'text_wrap': True})
            title_style4.set_border_color('black')
            table_header = workbook.add_format(
            {'font_name': 'Arial','font_size': 12, 'bold':10,
             'align': 'center','font_color': '#3b5a90','border':0, 'valign': 'vcenter','bg_color': 'white'})
            table_content = workbook.add_format(
            {'font_name': 'Arial','font_size': 10, 'font_color': 'black','bold':10,
             'align': 'center','color': 'black','border':0, 'valign': 'vcenter','bg_color': 'white'})
            table_content.set_num_format('#,##0.00')
            sequence_format = workbook.add_format(
            {'font_name': 'Arial','font_size': 10, 'font_color': 'black','bold':10,
             'align': 'center','color': 'black','border':0, 'valign': 'vcenter','bg_color': 'white'})
            table_header2 = workbook.add_format(
            {'font_name': 'Arial','font_size': 12, 'bold':10,
             'align': 'right','font_color': '#3b5a90','border':0, 'valign': 'vcenter','bg_color': 'white'})
            report_title = 'Snabel al-meshaan' 
            y = 0
            x = 0
            sheet.set_row(y,20) 
            sheet.merge_range('A1:E1', report_title, title_style)
            y+=1
            sheet.set_row(y,20) 
            sheet.merge_range('A2:E2', 'ksa-Hail -saptco', title_style)
            y+=1
            sheet.set_row(y,20)
            sheet.merge_range('A3:E3', 'L:3353001291 TEL:065310101', title_style)
            sheet.merge_range('A4:E8', '', title_style)
            sheet.merge_range('Q1:Z99', '', title_style)
            company_image = io.BytesIO(base64.b64decode(self.env.company.logo))
            sheet.merge_range('F1:K7', '', title_style)
            
            sheet.insert_image('H1', self.env.company.logo, {'image_data': company_image, 'x_scale': 0.6, 'y_scale': 0.4})
            sheet.merge_range('L1:P1', 'مجموعة سنابل المشعان', title_style3)
            sheet.merge_range('L2:P2', 'السعودية-حائل - النقل الجماعي', title_style3)
            sheet.merge_range('L3:P3', 'س.ت:3353001291 ت:065310101', title_style3)
            sheet.merge_range('L4:P8', '', title_style)
            # sheet.merge_range('F8:K8', '', title_style)
            y=7
            sheet.set_row(y,40)
            sheet.merge_range('F8:K8', 'الاقرار الضريبي لضريبة القيمة المضافة تحليلي', title_style4)
            sheet.merge_range('A9:P10', '', title_style)
            y=10
            sheet.set_row(y,30) 
            x=0
            sheet.merge_range(y, x,y,x+2,str(self.end_date), table_header)
            x+=3
            sheet.write(y, x, 'إلى', table_content)
            x+=3
            sheet.merge_range(y, x,y,x+2,str(self.start_date), table_header)
            x+=3
            sheet.write(y, x, 'من', table_content)
            x+=3
            sheet.merge_range('E11:F11', '', title_style)
            sheet.merge_range('K11:L11', '', title_style)
            sheet.merge_range('K11:O11', 'المشتريات الخاضعة للنسبة الاساسية', table_header2)
            sheet.write('P11', 'النوع', table_header2)
            y=11
            x=0
            sheet.set_row(y,30) 
            sheet.set_column(x,x,5)
            sheet.set_column(1,1,5)
            sheet.set_column(2,2,5) 
            sheet.merge_range(y, x,y,x+2, 'المبلغ بعد الضريبة', table_header)
            x+=3
            sheet.set_column(x,x,5)
            sheet.set_column(x+1,x+1,5)
            sheet.set_column(x+2,x+2,5) 
            sheet.merge_range(y, x,y,x+2, 'الضريبة', table_header)
            x+=3
            sheet.set_column(x,x,5)
            sheet.set_column(x+1,x+1,5) 
            sheet.merge_range(y, x,y,x+1, 'المبلغ قبل الضريبة', table_header)
            x+=2
            sheet.set_column(x,x,5)
            sheet.set_column(x+1,x+1,5) 
            sheet.merge_range(y, x,y,x+1, 'ملف ضريبي', table_header)
            x+=2
            sheet.set_column(x,x,10)
            sheet.write(y, x, 'المورد / العميل', table_header)
            x+=1
            sheet.set_column(x,x,10)
            sheet.write(y, x, 'رقم الفاتورة', table_header)
            x+=1
            sheet.set_column(x,x,10)
            sheet.write(y, x, 'الشرح الخاص', table_header)
            x+=1
            sheet.set_column(x,x,10)
            sheet.write(y, x, 'القيد', table_header)
            x+=1
            sheet.set_column(x,x,10)
            sheet.write(y, x, 'تاريخ القيد', table_header)
            x+=1
            sheet.set_column(x,x,5)
            sheet.write(y, x, 'م', table_header)
            
            sequence=1
            for record in result:
                partner_id = self.env['res.partner'].search([('id','=',record[3])],limit=1)
                y+=1
                x=0
                sheet.set_row(y,25) 
                sheet.merge_range(y, x,y,x+2, record[0], table_content)
                x+=3
                sheet.merge_range(y, x,y,x+2, record[1], table_content)
                x+=3
                sheet.merge_range(y, x,y,x+1, record[2], table_content)
                x+=2
                sheet.merge_range(y, x,y,x+1, partner_id.vat, table_content)
                x+=2
                sheet.write(y, x, partner_id.name, table_content)
                x+=1
                sheet.write(y, x,record[4], table_content)
                x+=1
                sheet.set_column(x,x,20) 
                sheet.write(y, x,record[5], table_content)
                x+=1
                sheet.write(y, x,record[4], table_content)
                x+=1
                sheet.write(y, x,str(record[6]), table_content)
                x+=1
                sheet.write(y, x,sequence, sequence_format)
                x+=1

            
            workbook.close()
            file_download = base64.b64encode(output.getvalue())
            output.close()
            wizardmodel = self.env['wiz.excel.reports']
            res_id = wizardmodel.create({'name': 'Tax Return Report', 'file_download': file_download})
            return {
                    'name': 'Files to Download',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'wiz.excel.reports',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                    'res_id': res_id.id,
                }
        else:
            data={
            'docs' : result,
            'start_date': self.start_date,
            'end_date': self.end_date
            }
            return self.env.ref('tax_return_report.tax_return_report_action').report_action(self, data)


class Wizexel(models.TransientModel):
    _name = 'wiz.excel.reports'

    name = fields.Char('File Name', size=256, readonly=True)
    file_download = fields.Binary('File to Download', readonly=True)

