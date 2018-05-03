# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_school_student(models.Model):

    _name = "scat.school.student"

    school_id = fields.Many2one('scat.school', string="Colegio", required=True)
    student_id = fields.Many2one('res.partner', string="Alumno", required=True)
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
