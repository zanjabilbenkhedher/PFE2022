# -*- coding: utf-8 -*-
# from odoo import http


# class Facture(http.Controller):
#     @http.route('/facture/facture/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/facture/facture/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('facture.listing', {
#             'root': '/facture/facture',
#             'objects': http.request.env['facture.facture'].search([]),
#         })

#     @http.route('/facture/facture/objects/<model("facture.facture"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('facture.object', {
#             'object': obj
#         })

from odoo import http
from odoo.http import request
import json
# from odoo.addons.website_sale.controllers.main import WebsiteSale


# class WebsiteSaleInherit(WebsiteSale):
#     @http.route([
#         '''/shop''',
#         '''/shop/page/<int:page>''',
#         '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
#         '''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>'''
#     ], type='http', auth="public", website=True)
#     def shop(self, page=0, category=None, search='', ppg=False, **post):
#         print("inherited odoo mates")
#         res = super(WebsiteSaleInherit, self).shop(page=0, category=None, search='', ppg=False, **post)


class Facture(http.Controller):
    # @http.route('/school/teachers/', website=True, auth='public')
    # def index(self, **kw):
    #     patients = request.env['school.teacher'].sudo().search([])
    #     return request.render("om_school.patients_page", {
    #         'patient': patients,
    #     })

    @http.route('/update_facture', type="json", auth='user', )
    def update_teacher(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                data = {}
                patient = request.env['facture.model.activity'].sudo().search([('id', '=', rec['id'])])
                if patient:
                    patient.sudo().write(rec)
                    data = {
                        'compare': patient.compare,
                    }
                args = {
                    'message': 'success',
                    'success': 'True',
                    'response': data,
                }
        return args


    @http.route('/get_factures', type="json", auth='public', csrf=False )
    def get_all_factures(self):
        # get all teachers
        teachers_rec = request.env['facture.model.activity'].search([])
        teachers = []
        for rec in teachers_rec:
            # print("rec.image", type(rec.image))
            vals = {
                'id': rec.id,
                'compare': rec.compare,
                # 'subject': rec.subject_id.name,
                # 'phone': rec.phone_number,
                # 'image': rec.image,
            }
            teachers.append(vals)
        data = {
            'status': "200",
            'message': "success",
            'response': teachers,
        }
        return data

