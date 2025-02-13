# -*- coding: utf-8 -*-
{
    'name': 'HR Attendance Geofence',
    'version': '13.0.1.0.1',
    'author': 'Resoos',
    'category': 'HR',
    'website': 'http://www.resoos.com/modules/hr',
    'description': """
Geofence of Employee Atendance
==============================
This module determines the geofence state of employee check in/out. The main functionalities are:

1. computes current employee location and compares that with geofence area in order to determine employee attendance state whether it is inside or outside geofence area
2. sends notification by email of calculated state to customer
""",
    'depends': [
        'web_google_maps_drawing',
        'hr_attendance',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/attendance_count.xml',
        'views/hr_attendance_area_view.xml',
        'views/hr_attendance_view.xml',
        # 'views/assets.xml',
        'report/attendance_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'calculate_attendance_geo_state/static/src/js/attendance_geolocation.js',
        ],
    }, 
    "external_dependencies": {"python" : ["shapely","geocoder"]},
    'installable': True
}
