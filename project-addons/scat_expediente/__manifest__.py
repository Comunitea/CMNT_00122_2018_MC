# -*- coding: utf-8 -*-

{
    'name': 'scat_expediente',
    'version': '10.0',
    'author': "Comunitea",
    'license': 'AGPL-3',
    'summary': 'Módulo Expediente',
    'depends': ['base',],
    'description': """
Modulo Expediente
Gestión de los expedientes de los colegios
""",
    'data': ['views/scat_expediente_view.xml',
              'security/ir.model.access.csv',],
    'installable': True,
    'auto_install': False,
}
