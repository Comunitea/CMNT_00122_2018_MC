# -*- coding: utf-8 -*-

{
    'name': 'scat_holidays',
    'version': '10.0',
    'author': "Comunitea",
    'license': 'AGPL-3',
    'summary': 'Módulo Vacaciones',
    'depends': ['base', 'project', 'scat_school'],
    'description': """
Modulo Vacaciones
Gestión de las vacaciones de los colegios
""",
    'data': ['views/scat_holidays_view.xml',
            'views/scat_school_view.xml',
              'security/ir.model.access.csv',],
    'installable': True,
    'auto_install': False,
}
