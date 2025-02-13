# -*- coding: utf-8 -*-
{
    'name': 'Web Google Maps',
    'version': '13.0.1.0.0',
    'author': 'Yopi Angi',
    'license': 'AGPL-3',
    'maintainer': 'Yopi Angi<yopiangi@gmail.com>',
    'support': 'yopiangi@gmail.com',
    'category': 'Extra Tools',
    'description': """
Web Google Map and google places autocomplete address form
==========================================================

This module brings three features:
1. Allows user to view all partners addresses on google maps.
2. Enabled google places autocomplete address form into partner
form view, it provide autocomplete feature when typing address of partner
""",
    'depends': [
        'base_setup',
        'base_geolocalize',
    ],
    'website': '',
    'data': [
        'data/google_maps_libraries.xml',
        'views/google_places_template.xml',
        'views/res_partner.xml',
        'views/res_config_settings.xml'
    ],
    'assets': {
        'web.assets_backend': [
            "web_google_maps/static/src/scss/web_maps.scss",
            "web_google_maps/static/src/scss/web_maps_mobile.scss",
            "web_google_maps/static/src/js/view/map/map_model.js",
            "web_google_maps/static/src/js/view/map/map_controller.js",
            "web_google_maps/static/src/js/view/map/map_renderer.js",
            "web_google_maps/static/src/js/view/map/map_view.js",
            "web_google_maps/static/src/js/view/view_registry.js",
            "web_google_maps/static/src/js/fields/relational_fields.js",
            "web_google_maps/static/src/js/widgets/utils.js",
            "web_google_maps/static/src/js/widgets/gplaces_autocomplete.js",
            "web_google_maps/static/src/js/widgets/fields_registry.js",
        ],
        'web.assets_qweb': [
            "web_google_maps/static/src/xml/widget_places.xml"
        ]
    },
    'demo': [],
    'images': ['static/description/thumbnails.png'],
    # 'qweb': ['static/src/xml/widget_places.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'uninstall_hook': 'uninstall_hook',
}