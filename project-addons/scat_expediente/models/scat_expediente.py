# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_expediente(models.Model):

    _name = "scat_expediente"

    n_expediente = fields.Integer(string="Nº de expediente", required= True)
    client= fields.Char(string="Cliente")
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
    school_ids = fields.Many2many('project.project', string="Colegio/s")
