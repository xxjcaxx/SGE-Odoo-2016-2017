# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class proves_decoradors(models.Model):
     _name = 'proves_decoradors.proves_decoradors'

     name = fields.Char()
     value = fields.Integer()
     valuedepends = fields.Float(compute="_value_depends", store=False)
     valuemulti = fields.Float(compute="_value_multi", store=False)
     valueone = fields.Float(compute="_value_one", store=False)
     valuemodel = fields.Float(compute="_value_model", store=False)
     description = fields.Text()

     @api.depends('value')
     def _value_depends(self):
         print "\033[91mSelf en @api.depends: \033[0m" + str(self)
         for record in self:
             record.valuedepends = float(record.value) / 100

     @api.multi
     def _value_multi(self):
         print "\033[92mSelf en @api.multi:\033[0m " + str(self)
         for record in self:
             record.valuemulti = float(record.value) / 10

     @api.one
     def _value_one(self):
         print "\033[93mSelf en @api.one:\033[0m " + str(self)
         self.valueone = float(self.value) / 20

     @api.model
     def _value_model(self):
         print "\033[94mSelf en @api.model:\033[0m " + str(self)
         for record in self:
             record.valuemodel = float(record.value) / 30

     @api.constrains('value')
     def _check_value(self):
         print "\033[95mSelf en @api.constrains:\033[0m " + str(self)
         for record in self:
             if record.value > 1000:
               raise ValidationError("Deuria ser menys que 1000 %s" % record.value)

     @api.onchange('value')
     def _onchange_value(self):
         print "\033[95mSelf en @api.onchange:\033[0m " + str(self)
         self.description = str(self.value)
 
