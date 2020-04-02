# -*- coding: utf-8 -*-
{
    'name': 'Get Fshare Direct Link',
    'version': '13.0',
    'category': 'Web',
    "license": "OPL-1",
    'description': """
        Allow to get Fshare link via web
    """,
    'author': 'Felix Consulting',
    'depends': [
        'base',
        'website',
    ],
    'data': [
        "security/ir_access_model.xml",
        "views/fshare_connector_view.xml",
        "views/fshare_page_template.xml",
        "views/fshare_page_assets.xml",
        "views/fshare_page_menu.xml"
    ],

    'test': [],
    'demo': [],
    'qweb': [
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'active': False,
    'application': False,
}
