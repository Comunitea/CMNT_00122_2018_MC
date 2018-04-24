# -*- coding: utf-8 -*-
from odoo import api, fields, models

class scat_student(models.Model):
    _name = "scat.student"

    name = fields.Many2one('res.partner', string="Alumno", required=True)

    school = fields.Many2one('project.project', string="Colegio", required=True)

    month = fields.Char(string="Mes", required=True)

    year = fields.Char(string="Año", required=True)

    dia1 = fields.Boolean(string="Día 1")
    dia2 = fields.Boolean(string="Día 2")
    dia3 = fields.Boolean(string="Día 3")
    dia4 = fields.Boolean(string="Día 4")
    dia5 = fields.Boolean(string="Día 5")
    dia6 = fields.Boolean(string="Día 6")
    dia7 = fields.Boolean(string="Día 7")
    dia8 = fields.Boolean(string="Día 8")
    dia9 = fields.Boolean(string="Día 9")
    dia10 = fields.Boolean(string="Día 10")
    dia11 = fields.Boolean(string="Día 11")
    dia12 = fields.Boolean(string="Día 12")
    dia13 = fields.Boolean(string="Día 13")
    dia14 = fields.Boolean(string="Día 14")
    dia15 = fields.Boolean(string="Día 15")
    dia16 = fields.Boolean(string="Día 16")
    dia17 = fields.Boolean(string="Día 17")
    dia18 = fields.Boolean(string="Día 18")
    dia19 = fields.Boolean(string="Día 19")
    dia20 = fields.Boolean(string="Día 20")
    dia21 = fields.Boolean(string="Día 21")
    dia22 = fields.Boolean(string="Día 22")
    dia23 = fields.Boolean(string="Día 23")
    dia24 = fields.Boolean(string="Día 24")
    dia25 = fields.Boolean(string="Día 25")
    dia26 = fields.Boolean(string="Día 26")
    dia27 = fields.Boolean(string="Día 27")
    dia28 = fields.Boolean(string="Día 28")
    dia29 = fields.Boolean(string="Día 29")
    dia30 = fields.Boolean(string="Día 30")
    dia31 = fields.Boolean(string="Día 31")
