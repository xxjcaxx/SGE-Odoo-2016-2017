# -*- coding: utf-8 -*-
from openerp import http

# class ProvesComputed(http.Controller):
#     @http.route('/proves_computed/proves_computed/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/proves_computed/proves_computed/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('proves_computed.listing', {
#             'root': '/proves_computed/proves_computed',
#             'objects': http.request.env['proves_computed.proves_computed'].search([]),
#         })

#     @http.route('/proves_computed/proves_computed/objects/<model("proves_computed.proves_computed"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('proves_computed.object', {
#             'object': obj
#         })