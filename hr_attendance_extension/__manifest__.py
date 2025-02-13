# -*- coding: utf-8 -*-
{
    'name': "HR Attendance Extension (Saudi)",

    'summary': """hr attendance base customization""",

    'description': """
        hr attendance base customization
    """,

    'author': "",
    'category': 'Human Resources/Attendance',
    'version': '15.0',

    'depends': ['hr_attendance', 'hr_payroll_extension'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/payroll_data.xml',
        'data/salary_rules.xml',
        'views/hr_attendance.xml',
        'views/attendance_deduction_view.xml',
        'views/hr_sheet_print.xml',
        'views/hr_attendance_rules.xml'
    ],
    
}
