# -*- coding: utf-8 -*-

{
    'name': 'Payroll Batch Report',
    'version': '1.0',
    'description': 'An excel report of payslips in a bactch',
    'summary': '',
    'author': 'Nasreldin Omer',
    'website': 'nasrom9@gmail.com',
    'license': 'LGPL-3',
    'category': 'HR',
    'depends': [ 'hr_payroll', 'report_xlsx'],
    'data': [

               'security/ir.model.access.csv',
               'report/payroll_batch_report.xml',
               'wizard/payroll_report_wizard_view.xml',
               'views/hr_salary_rule_view.xml',

    ],
    
    'auto_install': False,
    'application': False,
}