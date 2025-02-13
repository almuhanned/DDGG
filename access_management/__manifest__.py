# -*- coding: utf-8 -*-
#################################################################################
# Author      : Ashish Hirpara (<www.ashish-hirpara.com>)
# Copyright(c): 2021-22
# All Rights Reserved.
#
# This module is copyright property of the author mentioned above.
# You can't redistribute/reshare/recreate it for any purpose.
#
#################################################################################

{
    'name': 'Access Management',
    'version': '15.0.3.0.0',
    'sequence': 5,
    'author': 'Archana Prasad',
    'license': 'OPL-1',
    'category': 'Extra Tools',
    'website': '',
    'summary': """All In One Access Management App for setting the correct access rights for fields, models, menus, views for any module and for any user.
        All in one access management App,
        Easier then Record rules setup,
        Centralize access rules,
        User wise access rules,
        Show only what is needed for users,
        Access rules setup,
        Easy access rights setup, Hide Any Menu, Any Field, Any Report, Any Button,
        Easy To Configure,
        
        Main Features:-
        Hide fields,
        Hide Buttons,
        Hide Tabs,
        Hide views,
        Hide Contacts,
        Hide Menus,
        Hide submenus,
        Hide sub-menus,
        Hide reports,
        Hide actions,
        Hide server actions,
        Hide import,
        Hide delete,
        Hide archive,
        Hide Tree view, 
        Hide Form view, 
        Hide Kanban view, 
        Hide Calendar view, 
        Hide Pivot,
        Hide Graph view,
        Hide Apps,
        Hide object buttons,
        Hide action buttons,
        Hide smart buttons,
        Readonly Any Field,
        read only user,
        readonly user,
        Hide create,
        Hide duplicate,
        Control every fields,
        Control every views,
        Control every buttons,
        Control every actions.
        
        Multi Company supported.
        """,
    
    'description':"""

    """,
    'data':[
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'data/view_data.xml',
        'views/access_management_view.xml',
        'views/res_users_view.xml',
        'views/store_model_nodes_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/access_management/static/src/js/action_items.js',
            "/access_management/static/src/js/widget/DomainSelector.js",
            "/access_management/static/src/js/widget/ModelRecordSelector.js",
        ],
        
    },
    'depends':['web'],
    'post_init_hook': 'post_install_action_dup_hook',
    'application': True,
    'installable': True,
    'auto_install': False,
}
