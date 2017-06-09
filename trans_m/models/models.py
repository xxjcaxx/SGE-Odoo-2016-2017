# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime , date
from dateutil import parser

#creamos una clase que herede de sale.order para añadir un campo
class presupuesto(models.Model):
     _inherit = 'sale.order'
     _name = 'sale.order'

     travel= fields.Many2one('purchase.order', onlelete='cascade')
     
     def crear_factura(self):
       #solo te creara la factura si no esta creada todavia
       if(self.invoice_status != "invoiced"):
          #necesitamos que el estado est en to invoice para poder entrar en el metodo de sale
          self.invoice_status = "to invoice"
          self.state = "sale"
          for line in self.order_line:
            line.invoice_status = "to invoice"
          #creamos la factura y sus lineas
          invoice_id=self.action_invoice_create()
          #creamos todos los campos que son especificos del container
          invoice=self.env['account.invoice'].browse(invoice_id)
          print invoice
          invoice.write({'travel': self.travel.name})
          for line in invoice.invoice_line_ids:
            for oline in self.order_line:
              line.write({'is_container': oline.is_container,'tipe': oline.tipe,'weight': oline.weight,'receiver': oline.receiver.name,'progress': oline.progress})


class factura(models.Model):
     _inherit = 'account.invoice'
     _name = 'account.invoice'

     travel= fields.Char(string='Travel')
     is_paid=fields.Boolean()

#container facturado
class containerf(models.Model):
     _inherit = 'account.invoice.line'
     _name = 'account.invoice.line'
     

     is_container=fields.Boolean()
     tipe = fields.Selection([('1','Basic'),('2','Intermediate'),('3','Completed')])
     description = fields.Char()
     weight = fields.Float()
     receiver = fields.Char(string='Receiver')
     progress = fields.Float()
     travel = fields.Char(string='Travel',related='invoice_id.travel',readonly=True)  
    
#container pedido
class container(models.Model):
     _inherit = 'sale.order.line'
     _name = 'sale.order.line'
     

     is_container=fields.Boolean()
     tipe = fields.Selection([('1','Basic'),('2','Intermediate'),('3','Completed')])
     description = fields.Char()
     weight = fields.Float()
     receiver = fields.Many2one('res.partner')
     progress = fields.Float()
     client = fields.Many2one('res.partner')
     ready = fields.Boolean()
     travel = fields.Char(string='Travel',related='order_id.travel.name',readonly=True)
     
     
    
     #si el travel esta lleno con su maximo de containers no te deja añadir un container
     @api.constrains('travel')
     def _check_full_travel(self):
       for record in self:
         if len(record.travel.containers) > record.travel.ship.maxim_containers:
            raise ValidationError("The travel is full, maxim number of containers= %s" % record.travel.ship.maxim_containers)
#ready automatico cuando se cumpla pagado y progress
     @api.onchange('progress')
     def _check_ready(self):
       for record in self:
         if record.progress== 100:
            record.ready=True
     #sobreescribimos al modificar progress de un record
     @api.multi
     def write(self, values):
       if values.get('progress'):
          self.order_id.travel.crear_registro()
       return super(container, self).write(values)

     #sobreescribimos al crear un record
     @api.model
     def create(self, values):
       new_id = super(container, self).create(values)
       self.order_id.travel.crear_registro()
       return new_id 

 
class ship(models.Model):
     _inherit = 'res.partner'
     _name = 'res.partner'
     photo = fields.Binary('foto')
     name = fields.Char()
     is_ship = fields.Boolean()
     maxim_containers = fields.Integer()
     travels = fields.One2many('purchase.order','ship')
     travelling = fields.Boolean(compute='_is_out')

#calcular el boolean travelling para mostrar por colores o filtrar los que han salido o los que no
     @api.depends('travels')
     def _is_out(self):
       for record in self:
         record.travelling = False
         for travel in record.travels:
           if travel.progress > 0 and travel.progress < 100:
              record.travelling = True
    

class travel(models.Model):
     _inherit = 'purchase.order'
     _name = 'purchase.order'

     city_origin = fields.Many2one('res.country')
     destination = fields.Many2one('res.country')
     in_travel= fields.Boolean()
     progress= fields.Float(compute='_calculate_progress')
     ship = fields.Many2one('res.partner', onlelete='restrict')
     total_weight = fields.Float()
     origin_date = fields.Date()
     destination_date = fields.Date()
     orders = fields.One2many('sale.order','travel')
     containers = fields.One2many('sale.order.line', string="Containers", compute='_list_containers')
     containers_nr = fields.One2many('sale.order.line', string="Containers not ready", compute='_list_containersnr')
     loading_progress = fields.Float(compute='_calculate_loading_progress') 
     ready = fields.Boolean(compute='_check_ready') 
     invoices = fields.One2many('account.invoice','travel')
     registros = fields.One2many('trans_m.registro','travel')#,compute='_get_registros'

#metodo listar todos los containers
     @api.one
     def _list_containers(self):
       for record in self:
         lista_ids=self.env['sale.order.line']
         for pedido in record.orders:
           lista_pedido=self.env["sale.order.line"].search([("is_container", "=","True"),("order_id", "=",pedido.id)])
           lista_ids=lista_ids+lista_pedido
         record.containers = lista_ids

#metodo listar todos los containers not ready
     @api.one
     def _list_containersnr(self):
       for record in self:
         lista_ids=self.env['sale.order.line']
         for c in record.containers:
           lista_c=self.env["sale.order.line"].search([("id", "=",c.id),("ready", "!=","True")])
           lista_ids=lista_ids+lista_c
         record.containers_nr = lista_ids

#constrain check full travel para añadir containers
     @api.constrains('containers')
     def _check_full_travel(self):
       for record in self:
         if len(record.containers) > record.ship.maxim_containers:
            raise ValidationError("The travel is full, maxim number of containers= %s" % record.ship.maxim_containers)
#constrain origin date no se pondra sino esta el travel ready    
     @api.constrains('origin_date')
     def _check_ready_travel(self):
       for record in self:
         for c in record.containers:
           if c.ready == False:
            raise ValidationError("The travel isn't ready yet")
#metodo que gestiona cuando se calcula el progreso y que pasa pero llama otro progreso auxiliar para calcular  
     @api.depends('progress')
     def _calculate_progress(self):
       for record in self:
           if record.origin_date != False and record.destination_date != False:
             now = datetime.today()#fecha actual
             date1 = parser.parse(record.destination_date) #los field son strings
             date2 = parser.parse(record.origin_date)
             daysDiff = (date1-date2).days#diferencia entre fecha llegada y partida
             nowDiff = (now-date2).days#diferencia entre hoy y fecha partida
             #vamos a filtrar el error de dividir por 0
             aux = 0
             if daysDiff > 0:
               aux = (daysDiff - nowDiff)/float(daysDiff)
             #mostramos el porcentaje correcto
             porcentaje = 1 - aux
             record.progress =porcentaje*100
             #in_travel
             record.in_travel = False
             record.write({'in_travel': False })
             if record.progress > 0 and record.progress <100:
                record.in_travel = True
                record.write({'in_travel': True })
             else:
                record.progress = 0
       

#calcular el progreso de carga 1
     @api.depends('loading_progress')
     def _calculate_loading_progress(self):
       for record in self:
         record.loading_progress = record.calcular_progress()
       
#calcula si el travel esta ready es invisible solo para filtros o colores
     @api.depends('ready')
     def _check_ready(self):
       for record in self:
         record.ready = False
         bandera = True
         for c in record.containers:
           if c.ready == False:
             bandera = False
         if len(record.containers) == record.ship.maxim_containers and bandera == True:
           record.ready = True
         
#boton que pone todos los containers ready
     @api.multi
     def depart(self):
       for record in self:
         for c in record.containers:
           c.write({'ready':True})

#calcular el in_travel
     @api.depends('in_travel')
     def _calculate_in_travel(self):
       for record in self:
         record.in_travel = False
         record.write({'in_travel': False })
         if record.progress > 0 and record.progress <100:
            record.in_travel = True
            record.write({'in_travel': True })
     #añadir el campo destino del travel
     @api.multi
     def name_get(self):
       res=[]
       for i in self:
         res.append((i.id,str(i.name)+", "+str(i.destination.name)))
       return res

     #sobreescribimos al modificar un record
     @api.multi
     def write(self, values):
       new_id = super(travel, self).write(values)
       if values.get('origin_date') and values.get('destination_date') :
         for pedido in self.orders:
           pedido.crear_factura()            
       return new_id
#metodo auxiliar que calcula el loading progress 
     def calcular_progress(self):
       progreso=0
       totalCont = 0
       suma_progresos=0
       if self.ship.maxim_containers > 0:
         print self.ship.maxim_containers
         for c in self.containers:
           totalCont= totalCont + 1
           suma_progresos= suma_progresos + c.progress
         if totalCont > 0:
           progreso= suma_progresos / totalCont
       return progreso  
#antes de crear registro necesitamos calcular progress ya que es computed field
     def crear_registro(self):
       progress=self.calcular_progress()
       #crear registro
       a=self.env["trans_m.registro"].create({'progress': progress, 'travel': self.id, 'date': datetime.now()})
#get todos los registros de este travel
 #    @api.one
 #    def _get_registros(self):
 #      self.registros=self.env["trans_m.registro"].search([('travel','=',self.id)])
  #     print self.registros
      
class registro(models.Model):
     _name = 'trans_m.registro'

     date = fields.Datetime()
     progress = fields.Float()
     travel = fields.Char()
     
