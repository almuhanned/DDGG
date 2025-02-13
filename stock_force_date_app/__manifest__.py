# -*- coding: utf-8 -*-
{
    'name': 'Force date in Stock Transfer and Inventory Adjustment',
    "author": "Edge Technologies",
    'version': '15.0.1.5',
    'live_test_url':"https://youtu.be/dPuODkkjbDA",
    "images":['static/description/main_screenshot.png'],
    'summary': "Stock Force Date Inventory Force Date Inventory Adjustment Force Date Stock Transfer Force Date Stock Picking Force Date Receipt Force Date Shipment Force Date Delivery Force Date in Stock Backdate Stock Back Date Inventory Back Date Receipt Back Date",
    'description': """ 
        This Odoo Module will helps You to Allow Stock Force Date in Picking Operations and Inventory Adjustment. Auto Pass Stock Force Date in Stock Move When Validate Picking Operations and Inventory Adjustment.
    """,
    "license" : "OPL-1",
    'depends': ['stock','purchase','purchase_stock','stock_account'],
    'data': [
        'security/stock_force_security.xml',
        'views/stock_inventory.xml',
        ],
    'installable': True,
    'auto_install': False,
    'price': 25,
    'currency': "EUR",
    'category': 'Warehouse',
}
