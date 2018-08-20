# -*- coding: utf-8 -*-
from odoo import fields, models


class ScatSchool(models.Model):

    _inherit = "scat.school"

    warehouse_id = fields.Many2one("stock.warehouse", u"Almacén")
    rotative_menu_id = fields.Many2one("scat.menu.rotative",
                                       u"Menú rotativo")
