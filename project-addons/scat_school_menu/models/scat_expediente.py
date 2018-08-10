# -*- coding: utf-8 -*-

from odoo import models, fields


class ScatExpediente(models.Model):

    _inherit = "scat.expediente"

    rotative_menu_id = fields.Many2one("scat.menu.rotative",
                                       u"Menú rotativo")
