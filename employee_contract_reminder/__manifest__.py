# -*- coding: utf-8 -*-
{
    'name': "Employee Contract Reminder",

    'summary': """
        This module will send an email to the employee when the contract is about to expire.
    """,

    'description': """
        This module will send an email to the employee when the contract is about to expire.
    """,

    'author': "AMB",
    'website': "https://telenoc.org",
    'maintainers': ['AMB'],
    'license': 'LGPL-3',
    'category': 'Human Resources',
    'version': '15.0.1.0.1',
    'depends': ['base', 'hr_contract'],
    'data': [
        'security/res_groups.xml',
        'views/res_config_settings_views.xml',
        'data/ir_cron_data.xml',
        'data/mail_data.xml',
    ],
    'demo': [],
    'application': True,
}
