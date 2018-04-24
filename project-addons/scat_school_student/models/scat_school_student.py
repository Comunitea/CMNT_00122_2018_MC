# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_holidays(models.Model):

    _name = "scat.school.student"

    school = fields.Char(string="Colegio", required=True)
    student = fields.Char(string="Alumno", required=True)
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
