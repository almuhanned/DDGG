{
    'name': 'Hr Holiday Extend',
    'version': '15.0.1.0.0',
    'summary': """Hr Holiday Extend""",
    'description': 'Hr Holiday Extend',
    'category': 'Human Resources/Payroll',
    'depends': ['hr_payroll_holidays'],
    'data': [],
    'assets': {
        'web.assets_backend': [
            'hr_holiday_extend/static/src/js/**/*',
        ],
    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
