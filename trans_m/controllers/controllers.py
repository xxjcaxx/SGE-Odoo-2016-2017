# -*- coding: utf-8 -*-
from openerp import http

# class TransM(http.Controller):
#     @http.route('/trans_m/trans_m/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/trans_m/trans_m/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('trans_m.listing', {
#             'root': '/trans_m/trans_m',
#             'objects': http.request.env['trans_m.trans_m'].search([]),
#         })

#     @http.route('/trans_m/trans_m/objects/<model("trans_m.trans_m"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('trans_m.object', {
#             'object': obj
#         })