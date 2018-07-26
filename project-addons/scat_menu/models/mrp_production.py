# -*- coding: utf-8 -*-

from odoo import models, fields


class MrpProduction(models.Model):

    _inherit = "mrp.production"

    menu_line_id = fields.Many2one('scat.menu.line', 'Plato del menú',
                                   readonly=True)
