# -*- coding: utf-8 -*-


{
    "name": "Self Service Portal",
    "version": "0.1",
    "author": "Noptech",
    "description": "",
    "depends": ['portal', 'website','web', 'hr', 'hr_attendance', 'hr_reward_warning', 'hr_employee_updation', 'hr_holidays', 'project', 'hr_contract', 'hr_payroll', 'hr_expense'],
    "external_dependencies": {"python": ["geocoder"]},
    "data" : [
        'views/assets.xml',
        'views/hr_self_service_template.xml',
        'views/portal.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'hr_self_service/static/src/js/hr_selfservice.js',
        ],
    },

    'qweb': [],
    'installable': True,
    'application': True,
}
