# -*- coding: utf-8 -*-
from odoo import fields, models


class ScatSchool(models.Model):

    _inherit = "scat.school"

    warehouse_id = fields.Many2one("stock.warehouse", u"Almacén")
