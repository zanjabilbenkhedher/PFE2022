# -*- coding: utf-8 -*-
# from odoo import http


# class DetailsImage(http.Controller):
#     @http.route('/details_image/details_image/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/details_image/details_image/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('details_image.listing', {
#             'root': '/details_image/details_image',
#             'objects': http.request.env['details_image.details_image'].search([]),
#         })

#     @http.route('/details_image/details_image/objects/<model("details_image.details_image"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('details_image.object', {
#             'object': obj
#         })
