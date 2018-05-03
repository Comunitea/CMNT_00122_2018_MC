# -*- coding: utf-8 -*-
from odoo import fields, models, api

class ResPartner(models.Model):

    _inherit='res.partner'

    active_school_id=fields.Many2one('scat.school', 'Colegio activo',compute='get_active_school', store=True)
    school_ids=fields.One2many('scat.school.student', 'student_id', 'Colegios')



    @api.multi
    @api.depends('school_ids')
    def get_active_school(self):
        for partner in self:
            schools=partner.school_ids.filtered(lambda x:not x.end_date)
            partner.active_school_id=schools and schools[0].school_id.id or False
