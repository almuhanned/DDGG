# -*- coding: utf-8 -*-
{
    'name': 'Web Google Maps Drawing',
    'version': '13.0.1.0.0',
    'author': 'Yopi Angi',
    'license': 'AGPL-3',
    'maintainer': 'Yopi Angi',
    'support': 'yopiangi@gmail.com',
    'category': 'Extra Tools',
    'description': """
Web Google Maps Drawing
=======================

Allows users to draw polygons, rectangles, and circles on the map.
""",
    'depends': [
        'web_google_maps',
    ],
    'demo': [],
    'images': ['static/description/thumbnails.png'],
    'data': [
        'security/ir.model.access.csv',
        'data/google_maps_library.xml',
        # 'views/template.xml',
        'views/res_config_settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "web_google_maps_drawing/static/src/js/widget/field_gmaps_drawing.js",
            "web_google_maps_drawing/static/src/js/widget/fields_registry.js",
        ],
        'web.assets_qweb': [
            "web_google_maps_drawing/static/src/xml/drawing.xml"
        ]
    },
    # 'qweb': ['static/src/xml/drawing.xml'],
    'installable': True
}