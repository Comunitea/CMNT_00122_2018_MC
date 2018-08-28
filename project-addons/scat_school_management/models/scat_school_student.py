# -*- coding: utf-8 -*-
from odoo import fields, models, exceptions, api

class scat_school_student(models.Model):

    _name = "scat.school.student"

    school_id = fields.Many2one('scat.school', string="Colegio", required=True)
    student_id = fields.Many2one('res.partner', string="Alumno", required=True)
    start_date = fields.Date(string="Fecha inicio", required=True)
    end_date = fields.Date(string="Fecha fin")
    company_name = fields.Char(string = "Compañía")



    @api.onchange('school_id')
    def onchange_school_id_company(self):
        if self.school_id:
            expedientes= self.env['scat.expediente'].search([('school_ids', 'in', [self.school_id.id]), ('state', '=', 'open')])
            if expedientes:
                self.company_name = expedientes[0].company_id.name

            else:

                res={"warning":{"title":"Error", "message":"El colegio %s no tiene expediete abierto" % self.school_id.name}}
                self.school_id=False
                return res


    @api.constrains('start_date', 'end_date')
    @api.multi
    def addcolegio(self):
        for school in self:
            res=self.search([('student_id', '=', school.student_id.id ),('id','!=',school.id), ('end_date', '=', False)])
            if res:
                raise exceptions.ValidationError("Debe finalizar el colegio anterior de este alumno %s antes de crear uno nuevo" % school.student_id.name)
            else:
                res=self.search([('student_id', '=', school.student_id.id ),('id','!=',school.id), ('end_date', '>', school.start_date)])
                if res:
                    res.write({'end_date': school.start_date})
                    #raise exceptions.ValidationError("Debe finalizar el colegio anterior de este alumno %s antes de la fecha de inicio actual %s" % (school.student_id.name,school.start_date))
