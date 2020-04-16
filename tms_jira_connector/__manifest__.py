# -*- coding: utf-8 -*-
{
    'name': 'TMS - Jira Connector',
    'version': '13.0',
    'category': 'Web',
    "license": "OPL-1",
    'description': """
        TMS and Jira Connector
    """,
    'author': 'Felix Consulting',
    'depends': [
        'base',
        'website',
    ],
    'data': [
        "security/ir_access_model.xml",
        "views/jira_connector_view.xml",
    ],

    'test': [],
    'demo': [],
    'qweb': [
    ],
    'installable': True,
    'active': False,
    'application': False,
}
