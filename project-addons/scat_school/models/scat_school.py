# -*- coding: utf-8 -*-
from odoo import fields, models


class Project(models.Model):

        _name = "scat_school"
        _inherits = {'project.project': 'name'}

        code = fields.Char(string="Código", required=True)
        notes = fields.Text(string="Notas")
        school_id = fields.Many2one('project.project', string="Colegio", required=True)
