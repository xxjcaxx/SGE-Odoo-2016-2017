# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from datetime import date, datetime

class proves_computed(models.Model):
     _name = 'proves_computed.proves_computed'

     name = fields.Char()
     value = fields.Integer()
     image = fields.Binary(String="Image original")
     computedfloat = fields.Float(compute="_value_pc", store=True)
     computedchar = fields.Char(compute="_value_pc", store=False)
     medium_image = fields.Binary(compute="_redimensionar", store=True)
     small_image = fields.Binary(compute="_redimensionar", store=True)
     computedm2o = fields.Many2one('res.partner',compute="_value_pc", store=False)
     computedm2m = fields.Many2many(comodel_name='product.template',compute="_value_pc", store=False)
     computeddate = fields.Date(compute="_value_pc", store=False)
     computeddatetime = fields.Datetime(compute="_value_pc", store=False)
     
     description = fields.Text()

     @api.depends('value')
     def _value_pc(self):
      for r in self:
        r.computedfloat = float(r.value) / 100 
        r.computedchar = "("+str(r.value)+")"
        r.computedm2o = self.env['res.partner'].search([('id','=',r.value)]).id # Many2one espera un id, que és un camp Integer. 
        print '\033[93m'+str(self.env['product.product'].search([('id','>',r.value)]).ids)+'\033[0m'
        r.computedm2m = self.env['product.template'].search([('id','>',r.value)]).ids #Many2many espera un array d'ids. 
        # El codi comentat a continuació fa el mateix, per si volem fer altres coses dins del for.
        #ids = []
        #for t in self.env['product.template'].search([('id','>',r.value)]):
        # ids.append(t.id)
        #r.computedm2m = ids
 
        #r.computeddate = date.today() # Aquest depen de Python
        r.computeddate = fields.date.today() # Recomanem aquest, ja que és propi de la classe fields d'Odoo
        #r.computeddate = datetime.now()
        r.computeddatetime = fields.datetime.now()
        

     @api.depends('image')
     def _redimensionar(self):
       for r in self:
         image_original = r.image
         if image_original:
            images = tools.image_get_resized_images(image_original)
            r.medium_image = images['image_medium']                        
            r.small_image = images['image_small']                
         else:
            r.medium_image = ""                        
            r.small_image = ""
