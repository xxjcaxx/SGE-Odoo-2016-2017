# -*- coding: utf-8 -*-
from openerp import http

# class Cine(http.Controller):
#     @http.route('/cine/cine/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cine/cine/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cine.listing', {
#             'root': '/cine/cine',
#             'objects': http.request.env['cine.cine'].search([]),
#         })

#     @http.route('/cine/cine/objects/<model("cine.cine"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cine.object', {
#             'object': obj
#         })