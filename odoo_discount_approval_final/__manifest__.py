{
    'name': 'Odoo Discount Approval',
    'version': '1.4',
    'category': 'Sales',
    'summary': 'Manage discount approvals in sales quotations',
    'author': 'Custom Developer',
    'depends': ['sale', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'data/mail_template_data.xml',
    ],
    'installable': True,
    'application': False,
}