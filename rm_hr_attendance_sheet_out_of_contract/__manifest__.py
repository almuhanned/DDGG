# -*- coding: utf-8 -*-

{
    'name': 'HR Attendance Sheet Out of Contract',
    'version': '1.0',
    'summary': """ To add out of contract lines in attendance sheet """,
    'description': """
        To add out of contract lines in attendance sheet.
""",

    'author': 'TELENCO/Abdalrhman Ibrahim Ahmed',
    'support': 'abdalrhmanibrahim55@gmail.com',
    # 'images': ['static/description/icon.png'],
    'category': 'HR',
    'depends': ['rm_hr_attendance_sheet', 'hr_payslip_out_of_contract'],
    'data': [

                'views/hr_attendance_sheet_view.xml'

    ],
    'license': 'LGPL-3',
    'demo': [],
    'installable': True,
    'application': False,
}

