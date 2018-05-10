# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_expediente(models.Model):

    _name = "scat.expediente"

    n_expediente = fields.Integer(string="Nº de expediente", required= True)
    partner_id= fields.Many2one('res.partner', 'Cliente', required=True)
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
    school_ids = fields.Many2many('scat.school', string="Colegio/s")
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda s: s.env.user.company_id.id)
