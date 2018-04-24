# -*- coding: utf-8 -*-

{
    'name': 'scat_school',
    'version': '10.0',
    'author': "Comunitea",
    'license': 'AGPL-3',
    'summary': 'Sistema de Catering: Módulo colegios',
    'depends': ['base','project', ],
    'description': """
Modulo Colegios
Gestión de colegios
""",
    'data': ['views/scat_school_view.xml',
            'security/ir.model.access.csv',],
    'installable': True,
    'auto_install': False,
}
