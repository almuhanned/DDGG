from odoo import models, _


class PayrollBatchReport(models.AbstractModel):
    _name = 'report.payroll_report.payroll_report_xlsx'
    _description = 'Payroll Batch Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objects):
        for obj in objects:
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name[:31])
            sheet.set_column(2, 2, 40)
            sheet.set_column(3, 3, 20)
            sheet.set_column(4, 5, 40)
            sheet.set_column(6, 26, 20)
            bold = workbook.add_format({'bold': True, 'align': 'center'})
            left_align = workbook.add_format({'bold': True, 'align': 'left'})
            sheet.merge_range(0,0,0,26, 'Payroll Batch Report', bold)
            sheet.merge_range(2, 0, 2, 4, 'From: %s to %s' %(obj.date_start, obj.date_end), left_align)

            self.write_header(sheet, workbook)

            data = self.get_data(obj)
            row = 4
            serial = 1
            for key in data.keys():
                sheet.merge_range(row, 0, row, 26, key or 'Not Categorised', left_align)
                row += 1
                for line in data[key]:
                    self.write_line(sheet, workbook, line, row, serial)
                    row += 1
                    serial += 1

            


    def write_header(self, sheet, workbook):
        bold_header = workbook.add_format({'bold': True, 'bg_color': '#AAA', 'align': 'center'})
        sheet.write(3, 0, 'Serial No.', bold_header)
        sheet.write(3, 1, 'Project ID', bold_header)
        sheet.write(3, 2, 'Employee Name', bold_header)
        sheet.write(3, 3, 'Nationality', bold_header)
        sheet.write(3, 4, 'Department', bold_header)
        sheet.write(3, 5, 'Job Title', bold_header)
        sheet.write(3, 6, 'Joining Date', bold_header)
        sheet.write(3, 7, 'Contract Finish Date', bold_header)
        sheet.write(3, 8, 'Basic', bold_header)
        sheet.write(3, 9, 'OT Allowance', bold_header)
        sheet.write(3, 10, 'HRA', bold_header)
        sheet.write(3, 11, 'Transport Allowance', bold_header)
        sheet.write(3, 12, 'Food Allowance', bold_header)
        sheet.write(3, 13, 'Total Regular Month - SAR', bold_header)
        sheet.write(3, 14, 'Other Adjustments', bold_header)
        sheet.write(3, 15, 'Other Allowance', bold_header)
        sheet.write(3, 16, 'Additional Overtime', bold_header)
        sheet.write(3, 17, 'Unpaid Days Deduction', bold_header)
        sheet.write(3, 18, 'Gross Salary', bold_header)
        sheet.write(3, 19, 'Advance Payment', bold_header)
        sheet.write(3, 20, 'Traffic Penalty', bold_header)
        sheet.write(3, 21, 'Mobile Over Charges', bold_header)
        sheet.write(3, 22, 'GOSI Saudi Staff Share (9.75%)', bold_header)
        sheet.write(3, 23, 'Other Deduction', bold_header)
        sheet.write(3, 24, 'Total Deduction', bold_header)
        sheet.write(3, 25, 'Net Payment', bold_header)
        sheet.write(3, 26, 'Payment Mode', bold_header)

    def write_line(self, sheet, workbook, line, row, serial):
        regular_line = workbook.add_format({'bold': False, 'align': 'center'})
        sheet.write(row, 0, serial, regular_line)
        sheet.write(row, 1, line.get('project_id'), regular_line)
        sheet.write(row, 2, line.get('employee_name'), regular_line)
        sheet.write(row, 3, line.get('nationality'), regular_line)
        sheet.write(row, 4, line.get('department'), regular_line)
        sheet.write(row, 5, line.get('job_title'), regular_line)
        sheet.write(row, 6, line.get('joining_date'), regular_line)
        sheet.write(row, 7, line.get('contract_finish_date'), regular_line)
        sheet.write(row, 8, line.get('baisc'), regular_line)
        sheet.write(row, 9, line.get('overtime_allowance'), regular_line)
        sheet.write(row, 10, line.get('hra'), regular_line)
        sheet.write(row, 11, line.get('transport'), regular_line)
        sheet.write(row, 12, line.get('food'), regular_line)
        sheet.write(row, 13, line.get('total_regular_salary'), regular_line)
        sheet.write(row, 14, line.get('other_adjustment'), regular_line)
        sheet.write(row, 15, line.get('other_allowance'), regular_line)
        sheet.write(row, 16, line.get('addtional_overtime'), regular_line)
        sheet.write(row, 17, line.get('unpaid_days_deduction'), regular_line)
        sheet.write(row, 18, line.get('gross_salary'), regular_line)
        sheet.write(row, 19, line.get('advance_payment'), regular_line)
        sheet.write(row, 20, line.get('traffic_penality'), regular_line)
        sheet.write(row, 21, line.get('mobile_over_charges'), regular_line)
        sheet.write(row, 22, line.get('gosi'), regular_line)
        sheet.write(row, 23, line.get('other_deduction'), regular_line)
        sheet.write(row, 24, line.get('total_deduction'), regular_line)
        sheet.write(row, 25, line.get('net_payment'), regular_line)
        sheet.write(row, 26, line.get('payment_method'), regular_line)

    def get_data(self, batch):
        employee_type = {}
        
        for payslip in batch.slip_ids:
            contract_id = payslip.contract_id
            employee = payslip.employee_id
            basic = sum(payslip.line_ids.filtered(lambda line: line.code == 'BASIC').mapped('total'))
            ot_allowance = sum(payslip.line_ids.filtered(lambda line: line.code == 'OT100').mapped('total'))
            hra = sum(payslip.line_ids.filtered(lambda line: line.code == 'HOUALLOW').mapped('total'))
            transport = sum(payslip.line_ids.filtered(lambda line: line.code == 'TRAALLOW').mapped('total'))
            food = sum(payslip.line_ids.filtered(lambda line: line.code == 'FoodALLOW').mapped('total'))
            total_regular_salary = contract_id.total_salary
            other_adjustment = sum(payslip.line_ids.filtered(lambda line: line.code == 'REIMBURSEMENT').mapped('total'))
            other_allowance = sum(payslip.line_ids.filtered(lambda line: line.code == 'OTALLOW').mapped('total'))
            addtional_overtime = sum(payslip.line_ids.filtered(lambda line: line.code == 'OT200').mapped('total'))
            unpaid_days_deduction = sum(payslip.line_ids.filtered(lambda line: line.code == 'UNPAID').mapped('total'))
            gross_salary = sum(payslip.line_ids.filtered(lambda line: line.code == 'GROSS').mapped('total'))
            advance_payment = sum(payslip.line_ids.filtered(lambda line: line.code == 'ADVANCE').mapped('total'))
            traffic_penality = sum(payslip.line_ids.filtered(lambda line: line.code == 'TPENALTY').mapped('total'))
            mobile_over_charges = sum(payslip.line_ids.filtered(lambda line: line.code == 'MOVER').mapped('total'))
            gosi = sum(payslip.line_ids.filtered(lambda line: line.code == 'GOSI').mapped('total'))
            other_deduction = sum(payslip.line_ids.filtered(lambda line: line.code == 'DEDUCTION').mapped('total'))
            total_deduction = sum(payslip.line_ids.filtered(lambda line: line.category_id.name == 'Deduction').mapped('total'))
            net_payment = sum(payslip.line_ids.filtered(lambda line: line.code == 'NET').mapped('total'))
            if not contract_id.contract_type_id.name in employee_type:
                employee_type[contract_id.contract_type_id.name] = []
            employee_type[contract_id.contract_type_id.name].append({
                'project_id': employee.employee_code or '',
                'employee_name': employee.name or '',
                'nationality': employee.country_id.name or '',
                'department': employee.department_id.name or '',
                'job_title': employee.job_id.name or '',
                'joining_date': employee.join_date or '',
                'contract_finish_date': contract_id.date_end or '',
                'baisc': basic,
                'overtime_allowance': ot_allowance,
                'hra': hra,
                'transport': transport,
                'food': food,
                'total_regular_salary': total_regular_salary,
                'other_adjustment': other_adjustment,
                'other_allowance': other_allowance,
                'addtional_overtime': addtional_overtime,
                'unpaid_days_deduction': unpaid_days_deduction,
                'gross_salary': gross_salary,
                'advance_payment': advance_payment,
                'traffic_penality': traffic_penality,
                'mobile_over_charges': mobile_over_charges,
                'gosi': gosi,
                'other_deduction': other_deduction,
                'total_deduction': total_deduction,
                'net_payment': net_payment,
                'payment_method': 'Bank',
            })
        return employee_type
