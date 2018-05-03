# -*- coding: utf-8 -*-
from odoo import api, fields, models
from dateutil.rrule import MO, TU, WE, TH, FR, rrule, WEEKLY
from datetime import datetime
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
import calendar


class scat_student(models.Model):
    _name = "scat.student"
    _rec_name ='student_id'
    _order = "start_date desc,school_id"

    student_id = fields.Many2one('res.partner', string="Alumno", required=True)

    school_id = fields.Many2one('scat.school', string="Colegio", required=True)

    month = fields.Char(string="Mes", required=True)

    year = fields.Char(string="Año", required=True)
    start_date = fields.Date(readonly=True)



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



    @api.model
    def get_next_month(self):

        today = datetime.now()
        today = today+relativedelta(months=1)
        last_day = calendar.monthrange(today.year, today.month)[1]
        first_day=datetime(today.year, today.month, 1)
        last_date = datetime(today.year, today.month, last_day)



        for school in self.env['scat.school'].search([]):


            dias_festivos=self.dias_festivos(first_day, last_date,school)

            for student_seleccionado in self.env['res.partner'].search([('active_school_id', '=', school.id), ('x_ise_estado', '=', 'usuario'), ('parent_id', '!=', False)]):
                vals={'student_id': student_seleccionado.id, 'school_id': school.id, 'month': str(today.month), 'year': str(today.year), 'start_date': first_day.strftime('%Y-%m-%d')}
                if student_seleccionado.y_ise_s:
                    self.create(vals)

                else:
                    if student_seleccionado.y_ise_factura_aut:
                        dias = [MO, TU, WE, TH, FR]
                    else:
                        dias = []
                        if student_seleccionado.y_ise_l:
                            dias += [MO]
                        if student_seleccionado.y_ise_m:
                            dias += [TU]
                        if student_seleccionado.y_ise_x:
                            dias += [WE]
                        if student_seleccionado.y_ise_j:
                            dias += [TH]
                        if student_seleccionado.y_ise_v:
                            dias += [FR]

                    date_list = list(rrule(WEEKLY, dtstart=first_day, until=last_date, byweekday=dias))
                    days=set(date_list)-dias_festivos
                    new_vals = dict(vals)
                    for day in days:
                        new_vals['dia'+str(day.day)]=True


                    self.create(new_vals)



    def dias_festivos(self, first_day, last_date,school):

        domain=[('school_ids', 'in', [school.id]),('end_date', '>=', first_day.strftime('%Y-%m-%d')),('start_date','<=',last_date.strftime('%Y-%m-%d'))]


        lista_festivos=set()

        for festivo in self.env['scat.holidays'].search(domain):
            if festivo.end_date>last_date.strftime('%Y-%m-%d'):
                end_date=last_date
            else:
                end_date=datetime.strptime(festivo.end_date,'%Y-%m-%d')

            if festivo.start_date<first_day.strftime('%Y-%m-%d'):
                start_date=first_day
            else:
                start_date=datetime.strptime(festivo.start_date,'%Y-%m-%d')


            lista_fechas = [start_date + timedelta(days=d) for d in range((end_date - start_date).days + 1)]

            lista_festivos |= set(lista_fechas)



        return lista_festivos





    def recuento_dias(self):
        return len("dates")

