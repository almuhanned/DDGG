# -*- coding: utf-8 -*-
{
    'name': "Payroll Extension (Saudi)",

    'summary': """Customize payroll KSA bas""",

    'description': """
        Customize payroll KSA bas
    """,

    'author': "",
    'category': 'Human Resources/Payroll',
    'version': '15.0',

    'depends': ['hr_payroll', 'hr_contract','hr_payroll_account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/payslip_payment.xml',
        'views/hr_contract_views.xml',
        'views/hr_payslip.xml',
        'views/hr_payslip_batch.xml',
        'data/hr_payroll_structure_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_salary_rule_data.xml'
    ],
    
}
