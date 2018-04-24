# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_holidays(models.Model):

    _name = "scat_holidays"

    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
    description = fields.Text(string="Descripción")
    school_ids = fields.Many2many('project.project', string="Colegio/s")
