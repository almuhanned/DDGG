# -*- coding: utf-8 -*-
{
    'name': 'HR Employee Info Updation',
    'version' : '15.0.1.0',
    'summary': 'hr_employee_info_updation',
    'category': 'hr',
    'author' : 'Magdy,TeleNoc',
    'description': """
    hr_employee_info_updation
    """,
    'depends': ['hr', 'hr_payroll', 'hr_holidays'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'views/hr_payslip.xml',
    ]
}
