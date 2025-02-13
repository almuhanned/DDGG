__auther__ = 'Abdalrhman Ibrahim ^_^'

from odoo import models, _


class PayrollBatchReport(models.AbstractModel):
    _name = 'report.payroll_report.payroll_report_xlsx'
    _description = 'Payroll Payslip Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        report_name = "Payslips Report"
        form = data.get('form')
        from_date = form.get('from_date')
        salary_structure_id = self.env['hr.payroll.structure'].browse(int(form.get('salary_structure_id')[0]))
        to_date = form.get('to_date')
        payslip_ids = self.env['hr.payslip'].browse(data.get('payslip_ids'))
        sheet = workbook.add_worksheet(report_name)
        header_frmt = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#A9A9A9',
            'border': 3,
            'font_size': 13
        })

        value_header_frmt = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'border': 3,
            'font_size': 11
        })

        sub_header_frmt = workbook.add_format({
            'bold': True,
            'align': 'center',
            'valign': 'vcenter',
            'fg_color': '#f2f0f6',
            'border': 4,
            'font_size': 9
        })

        body_frmt = workbook.add_format({
            'valign': 'vcenter',
            'fg_color': '#FAEBD7',
            'border': 3,
            'font_size': 11
        })
        sheet.merge_range('A1:F2', salary_structure_id.name + ': ' + report_name, value_header_frmt)
        sheet.merge_range('A3:B3', 'From: %s' % from_date, sub_header_frmt)
        sheet.merge_range('D3:E3', 'To: %s' % to_date, sub_header_frmt)

        header_frmt.set_pattern(1)
        sheet.set_column(0, 9, 15)
        row_start = 5
        if payslip_ids:
            rules = self.get_structure_rule(salary_structure_id)
            sheet.write(row_start, 0, "Reference", sub_header_frmt)
            sheet.write(row_start, 1, "Badge ID", sub_header_frmt)
            sheet.write(row_start, 2, "Employee", sub_header_frmt)
            sheet.write(row_start, 3, "Identification No", sub_header_frmt)
            sheet.write(row_start, 4, "Work Location", sub_header_frmt)
            sheet.write(row_start, 5, "Nationality", sub_header_frmt)
            sheet.write(row_start, 6, "Department", sub_header_frmt)
            sheet.write(row_start, 7, "Job Title", sub_header_frmt)
            sheet.write(row_start, 8, "Join Date", sub_header_frmt)
            sheet.write(row_start, 9, "Contract End Date", sub_header_frmt)
            sheet.write(row_start, 10, "Bank Name", sub_header_frmt)
            sheet.write(row_start, 11, "IBAN Number", sub_header_frmt)
            colum1 = 12

            for rule in rules:
                sheet.write(row_start, colum1, rule.name, sub_header_frmt)
                colum1 += 1

            sheet.write(row_start, colum1, "Status", sub_header_frmt)

            row = row_start + 1
            for payslip in payslip_ids:
                sheet.write(row, 0, payslip.name, body_frmt)
                sheet.write(row, 1, payslip.employee_id.barcode, body_frmt)
                sheet.write(row, 2, payslip.employee_id.name, body_frmt)
                sheet.write(row, 3, payslip.employee_id.identification_id, body_frmt)
                sheet.write(row, 4, payslip.employee_id.work_location_id.name if payslip.employee_id.work_location_id else 'None', body_frmt)
                sheet.write(row, 5, payslip.employee_id.country_id.name, body_frmt)
                sheet.write(row, 6, payslip.employee_id.department_id.name, body_frmt)
                sheet.write(row, 7, payslip.employee_id.job_id.name, body_frmt)
                sheet.write(row, 8, str(payslip.employee_id.join_date), body_frmt)
                sheet.write(row, 9, str(payslip.employee_id.contract_id.date_end), body_frmt)
                sheet.write(row, 10, payslip.employee_id.bank_name, body_frmt)
                sheet.write(row, 11, payslip.employee_id.iban_number, body_frmt)
                colum2 = 12

                for rule in rules:
                    amount = 0.0
                    if rule.id in payslip.line_ids.mapped('salary_rule_id').ids:
                        line_id = payslip.line_ids.filtered(lambda line: line.salary_rule_id.id == rule.id)
                        if line_id:
                            amount = line_id.total
                    sheet.write(row, colum2, amount, body_frmt)
                    colum2 += 1

                state = str(dict(payslip.fields_get(allfields=['state'])['state']['selection'])[payslip.state])
                sheet.write(row, colum2, state, body_frmt)

                row += 1

    def get_structure_rule(self, structure_id):
        res = structure_id.rule_ids.filtered(lambda r: r.appears_on_report).sorted(key=lambda r: r.sequence)
        return res
