# -*- coding: utf-8 -*-
from openerp import http

# class ProvesDecoradors(http.Controller):
#     @http.route('/proves_decoradors/proves_decoradors/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proves_decoradors/proves_decoradors/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proves_decoradors.listing', {
#             'root': '/proves_decoradors/proves_decoradors',
#             'objects': http.request.env['proves_decoradors.proves_decoradors'].search([]),
#         })

#     @http.route('/proves_decoradors/proves_decoradors/objects/<model("proves_decoradors.proves_decoradors"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proves_decoradors.object', {
#             'object': obj
#         })