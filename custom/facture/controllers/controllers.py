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
