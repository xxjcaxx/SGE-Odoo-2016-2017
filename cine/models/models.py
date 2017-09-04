# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from dateutil.relativedelta import *
from openerp.exceptions import ValidationError
from datetime import timedelta, datetime

class cine(models.Model):
     _name = 'cine.cine'

     name = fields.Char()
     pais = fields.Many2one('res.country', string='Country')
     direccio = fields.Char(string='Address')
     description = fields.Text()
     sales = fields.One2many('cine.sala','cine',string='Theaters')
     empleats = fields.Many2many('hr.employee',string='Employees') 
     en_cartell = fields.Many2many('cine.pelicula',compute='_get_cartellera',string='Billboard') 
     sessions = fields.Many2many('cine.sessio',compute='_get_cartellera',string='Sessions') 
     projeccio = fields.Many2many('cine.sessio',compute='_get_cartellera',string='Current Projections') 
     #programacio (queda la vista i mostrar progrés)
     @api.multi
     def _get_cartellera(self):
      hui = fields.date.today()
      ara = fields.datetime.now()
      hui7 = fields.date.today()+relativedelta(days=+7)
      for cine in self:
       cartell = self.env['cine.sessio'].search([('sala.cine.id','=',cine.id),('dia','>=',hui),('dia','<',hui7)])
       sessions = self.env['cine.sessio'].search([('sala.cine.id','=',cine.id),('dia','=',hui)])
       projeccio = self.env['cine.sessio'].search([('sala.cine.id','=',cine.id),('dia','=',hui)])
       llista = []
       for p in projeccio:
         if p.projectantse(p.id):
           llista.append(p.id)
       cine.en_cartell=cartell.mapped('pelicula.id')
       cine.sessions=sessions.ids
       cine.projeccio=llista


class sala(models.Model):
     _name = 'cine.sala'

     name = fields.Char()
     cine = fields.Many2one('cine.cine',string='Cinema',ondelete='cascade')
     butaques = fields.One2many('cine.butaca','sala',string='Seats')

class sessio(models.Model):
     _name = 'cine.sessio'

     name = fields.Char(compute='_get_dia',store=True)
     sala = fields.Many2one('cine.sala',string='Theater',ondelete='set null')
     cine = fields.Many2one('cine.cine',store=False,string='Cinema')
     hora = fields.Datetime('Hour')
     dia = fields.Date(compute='_get_dia',store=True,string='Day')
     duracio = fields.Float(related='pelicula.duracio',string='Duration')
     pelicula = fields.Many2one('cine.pelicula',string='Movie',ondelete='restrict')
     pelicula_poster = fields.Binary(related='pelicula.poster',string='Movie poster')
     entrades = fields.One2many('cine.entrada','sessio', string='Tickets')
     projeccio = fields.Boolean(compute='_get_projeccio',store=False, string='Projection')
     percent_projeccio = fields.Float(compute='_get_projeccio',store=False, string='% Projection')

     @api.onchange('cine')
     def _filter_sala(self):
      #print self.cine
      return { 'domain': {'sala': [('cine','=',self.cine.id)]} }     


     @api.depends('sala','hora','pelicula')
     def _get_dia(self):
       for r in self:
         nombre="aun sin nombre"
         if r.sala and r.pelicula and r.hora:
           nombre=r.sala.name+" / "+r.pelicula.name+" / "+str(r.hora)
         r.name=nombre
         if r.hora:
           r.dia=r.hora
         r.name=nombre

     @api.depends('hora')
     def _get_projeccio(self):
      for p in self:
        pro=self.projectantse(p.id)
        p.projeccio=pro
        if pro==True:
         fmt = '%Y-%m-%d %H:%M:%S'
         d1 = datetime.strptime(p.hora, fmt)
         d2 = datetime.strptime(fields.Datetime.now(), fmt)
         print str(d1)+"-----"+str(d2)

         minsDiff = (d2-d1).seconds/60
         print minsDiff
         percent=tools.float_round((minsDiff/(p.pelicula.duracio*60))*100,precision_rounding=0.01)
        else:
         percent=0
        p.percent_projeccio = percent
        

     def projectantse(self,id):
       p = self.env['cine.sessio'].browse(id);
       if p.hora:
        fin = fields.Datetime.from_string(p.hora)+timedelta(hours=p.pelicula.duracio)
        #print type(fields.Datetime.from_string(p.hora))
        #print type(datetime.now())
        if fields.Datetime.from_string(p.hora) <= datetime.now() and fin >= datetime.now():
       	 return True
        else:
         return False
       else:
        return False
     
class pelicula(models.Model):
     _name = 'cine.pelicula'
     name = fields.Char()
     director = fields.Char()
     estreno = fields.Date('Release')
     poster = fields.Binary()
     sessions = fields.One2many('cine.sessio','pelicula')
     preu = fields.Float(default=7,string='Price') 
     duracio = fields.Float('Duration')
     encartell = fields.Boolean('Billboard') 
     # La manera poc elegant però efectiva de poder buscar en fields computed 
     encartell2 = fields.Boolean(compute='_get_encartell',store=False,string='Billboard')

     def _get_encartell(self):
      for p in self:
       session_posteriors=self.env['cine.sessio'].search_count([('hora','>',fields.Datetime.now()),('pelicula','=',p.id)])
       #print session_posteriors.mapped('name'))
       c =  (session_posteriors > 0)
       p.write({'encartell':c})
       p.encartell2 = c      

class butaca(models.Model):
     _name = 'cine.butaca'
     
     name = fields.Char(string="Position", compute='_get_position',store=True)
     fila = fields.Integer('Row')
     butaca = fields.Integer('Seat')
     sala = fields.Many2one('cine.sala',string='Theater',ondelete='cascade')
     @api.depends('fila','butaca')
     def _get_position(self):
       for r in self:
         if  r.fila and r.butaca:
           r.name="Fila: "+str(r.fila)+", Butaca: "+str(r.butaca)

class entrada(models.Model):
      _name = 'cine.entrada'
     
      name = fields.Char(string="Identification", compute='_get_id')
      butaca = fields.Many2one('cine.butaca',string='Seat', ondelete='set null')
      sessio = fields.Many2one('cine.sessio',string='Session')
      dia = fields.Date(related='sessio.dia',string='Dia', store=True) # per al graph
      aux_cine = fields.Many2one('cine.cine',store=False,string='Cinema')
      aux_sala = fields.Many2one('cine.sala',store=False,string='Theater')
      sala = fields.Many2one('cine.sala',related='sessio.sala',store=True,readonly=True,string='Theater')
      cine = fields.Many2one('cine.cine',related='sessio.sala.cine',store=True,readonly=True,string='Cinema')
      pelicula = fields.Many2one('cine.pelicula',related='sessio.pelicula',store=True,readonly=True,string='Movie')
      preu_graph = fields.Float(related='pelicula.preu', string='recaptacio' ,store=True) # per al graph
      preu = fields.Float('Price',compute="_get_price",search='_search_price',inverse='_set_price') 
      state = fields.Selection([
        ('creada', "Created"),
        ('reservada', "Reserved"),
        ('pagada', "Paid"),
      ], default='creada')
      descompte = fields.Selection([
        (0, "None"),
        (10, "Carnet Jove"),
        (20, "< 6 years"),
        (30, "Bonus"),
      ], default=0)

      @api.depends('butaca','sessio')
      def _get_id(self):
       for r in self:
         if r.sessio and r.butaca:
          r.name=r.butaca.sala.name+" "+r.butaca.name+": "+str(r.sessio.hora)

      @api.depends('pelicula','descompte')
      def _get_price(self):
        for r in self:
          price = r.pelicula.preu
          price = price - (price*r.descompte/100)
          r.preu = price

      def _search_price(self,operator,value): # De moment aquest search sols és per a ==
       preus = self.search([]).mapped(lambda e: [e.id , e.pelicula.preu - (e.pelicula.preu*e.descompte/100)]) # Un bon exemple de mapped en lambda
       print preus
       p = [ num[0] for num in preus if num[1] == value]  # condició if en una llista python sense fer un for (list comprehension)
       # també es pot provar en un filter() de python
       print p
       # p és una llista de les id que ja compleixen la condició, per tant sols cal fer que la id estiga en la llista.
       return [('id','in',p)]

      def _set_price(self):
       self.pelicula.preu = self.preu  # Açò és un exemple, però està mal, ja que modifiques el preu de la peli en totes les sessions


      @api.constrains('butaca','sessio')
      def _check_repeticions(self):
        for r in self:
          if self.search_count([('butaca.id','=',r.butaca.id),('sessio.id','=',r.sessio.id)]) > 1:
            raise ValidationError("Repetida")
          if r.butaca.sala.id != r.sessio.sala.id:
            raise ValidationError("La butaca no és de la sala")

      @api.onchange('aux_cine')
      def _filter_cine(self):
        return { 'domain': {'aux_sala': [('cine','=',self.aux_cine.id)]} }     
      @api.onchange('aux_sala')
      def _filter_sala(self):
        return { 'domain': {'sessio': [('sala','=',self.aux_sala.id)]} }     
      @api.onchange('sessio')
      def _filter_sessio(self):
        butacas=self.env['cine.butaca'].search([('sala','=',self.sessio.sala.id)])
        print butacas 
        libres=[]
        for i in butacas:
         entradas=self.search_count([('butaca','=',i.id)])
         if entradas == 0:
          libres.append(i.id)
        print libres
        return { 'domain': {'butaca': [('id', 'in' , libres)]} } 
    
      @api.multi
      def change_state(self):
       for r in self:
        if r.state == 'creada':
          r.write({'state':'reservada'})
        elif r.state == 'reservada':
          r.write({'state':'pagada'})
        elif r.state == 'pagada':
          r.write({'state':'creada'})
            

class wizSessions(models.TransientModel):
      _name = 'cine.wiz_sessions'
      def _default_cine(self):
         return self.env['cine.cine'].browse(self._context.get('active_id')) 
      cine=fields.Many2one('cine.cine',default=_default_cine)
      pelicules=fields.Many2many('cine.pelicula')
      dia=fields.Date() 
      state = fields.Selection([
        ('pelis', "Movie Selection"),
        ('dia', "Day Selection"),
      ], default='pelis')
 
      @api.multi
      def action_pelis(self):
        self.state = 'pelis'
        return { "type": "ir.actions.do_nothing", }

      @api.multi
      def action_dia(self):
        self.state = 'dia'
        return { "type": "ir.actions.do_nothing", }
      
      @api.multi
      def crear(self):
        sales=self.cine.sales.ids
        n_sales = len(sales)
        sala=0
        for i in self.pelicules:
         if sala<n_sales:
          sessio=self.dia+' 18:00:00'
          for j in range(0,3):
            s=self.env['cine.sessio'].create({'pelicula':i.id,'hora':sessio,'cine':self.cine.id,'sala':sales[sala]})
            sessio=(datetime.strptime(sessio, '%Y-%m-%d %H:%M:%S')+timedelta(hours=i.duracio)).strftime('%Y-%m-%d %H:%M:%S')
          sala = sala + 1
        return {}


class wizSessions2(models.TransientModel):
      _name = 'cine.wiz_sessions2'
      def _default_cine(self):
         return self.env['cine.cine'].browse(self._context.get('active_id')) 
      def _get_horainici(self):
        return fields.Date.today()+" 18:00:00"       
      cine=fields.Many2one('cine.cine',default=_default_cine)
      sala=fields.Many2one('cine.sala')
      pelicula=fields.Many2one('cine.pelicula')
      hora_inici=fields.Datetime(default=_get_horainici) 
      sessions=fields.Many2many('cine.sessio') # Falta afegir com a referència les sessions d'eixe dia en eixa sala.
      
      @api.onchange('sala')
      def lista_sessions(self):
        s=self.env['cine.sessio'].search([('dia','=',self.hora_inici)]).ids
        self.sessions = [(6,0,s)] 

      @api.multi
      def crear(self):
        sala=self.sala.id
        peli=self.pelicula.id
        s=self.env['cine.sessio'].create({'pelicula':peli,'hora':self.hora_inici,'cine':self.cine.id,'sala':sala})
        self.sessions = [(4,s.id)]
        fmt = '%Y-%m-%d %H:%M:%S'
        h = datetime.strptime(self.hora_inici, fmt)+timedelta(hours=+self.pelicula.duracio)
        self.hora_inici = h.strftime(fmt)
        return { "type": "ir.actions.do_nothing", }

class wizbutaques(models.TransientModel):
      _name = 'cine.wiz_butaques'
      def _default_sala(self):
         return self.env['cine.sala'].browse(self._context.get('active_id')) 
      sala=fields.Many2one('cine.sala',default=_default_sala)

      files=fields.Integer(default=10)
      butaques=fields.Integer(default=10)

      @api.multi
      def crear(self):
        sala=self.sala.id
        for i in range(0,self.files):
         for j in range(0,self.butaques):
            s=self.env['cine.butaca'].create({'sala':sala,'fila':i+1,'butaca':j+1})
        return {}

#TODO
# https://erflow.com/questions/9377402/insert-into-many2many-odoo-former-openerp
#https://www.odoocom/cumentation/9.0/reference/views.html#qweb https://www.odoo.com/es_ES/forum/ayuda-1/question/how-to-create-a-new-view-type-24330
