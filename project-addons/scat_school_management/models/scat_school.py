# -*- coding: utf-8 -*-
from odoo import fields, models


class scat_school(models.Model):

    _name = "scat.school"
    _inherits = {'project.project': 'school_id'}

    code = fields.Char("Referencia", required=True)
    notes = fields.Text(string="Notas")
    school_id = fields.Many2one('project.project', string="Colegio",
                                required=True, ondelete="cascade")
    state_id = fields.Many2one("res.country.state",
                               related="school_id.partner_id.state_id",
                               readonly=True)
    expedient_ids = fields.\
        Many2many(comodel_name='scat.expediente',
                  relation='scat_expediente_scat_school_rel',
                  column1='scat_school_id', column2='scat_expediente_id',
                  string="Expediente/s")


class AccountAnalyticAccount(models.Model):

    _inherit = "account.analytic.account"

    company_id = fields.Many2one('res.company', required=False)


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    company_id = fields.Many2one("res.company", related=None, string='Company',
                                 readonly=True,
                                 default=lambda s: s.env.user.company_id.id)
