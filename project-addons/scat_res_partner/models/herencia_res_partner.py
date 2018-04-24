# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models


class herencia_res_partner(models.Model):

    _inherit = "res.partner"
    x_ise_nie = fields.Char(string='NIE', required=False, help="Identificador del alumno")
    x_ise_estado = fields.Char(string='Estado', required=False)
    x_ise_centro = fields.Char(string='Centro', required=False)

    y_ise_factura_aut = fields.Boolean(string='y_ise_factura_aut', required=False)

    y_ise_l = fields.Boolean(string='Lunes', required=False)
    y_ise_m = fields.Boolean(string='Martes', required=False)
    y_ise_x = fields.Boolean(string='Miércoles', required=False)
    y_ise_j = fields.Boolean(string='Jueves', required=False)
    y_ise_v = fields.Boolean(string='Viernes', required=False)
    y_ise_s = fields.Boolean(string='Esporádico', required=False)
