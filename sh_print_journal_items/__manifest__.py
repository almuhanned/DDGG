# -*- coding: utf-8 -*-
{
    "name": "Print Journal Items",

    "author": "Softhealer Technologies",

    "license": "OPL-1",

    "website": "https://www.softhealer.com",

    "support": "support@softhealer.com",

    "version": "15.0.3",

    "category": "Accounting",

    "summary": "print journal items app, print multiple items module, print journal items, print journals, journal items report, print journal report, journal item report odoo",

    "description": """This module useful to print journal items.""",

    "depends":  ['account'],

    "data": [
            "security/ir.model.access.csv",
            "reports/report_account_journal_items.xml",
            "wizard/journal_item_xls_report_wizard.xml",
        ],
    "images": ["static/description/background.png", ],
    "live_test_url": "https://youtu.be/XtzBQQdQJtM", 
    "installable": True,
    "application": True,
    "auto_install": False,
    "price": 7,
    "currency": "EUR"

}
