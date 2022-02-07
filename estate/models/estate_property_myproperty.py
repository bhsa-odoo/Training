
from odoo import models,fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError,ValidationError



class EstatePropertyMyproperty(models.Model) :
    _name = 'estate.property.myproperty'
    _description = 'My Property'

    def _get_description(self) :
        if self.env.context.get('is_my_property') :
            return self.env.user.name + "'s property"

    name = fields.Char(string = "Property Name",default="Unknown",required=True,filter="1")
    description = fields.Text(default=_get_description)
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(),copy=False)
    expected_price = fields.Float() 
    selling_price = fields.Float(copy=False,readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north' , 'North'),
        ('south' , 'South'),
        ('east' , 'East'),
        ('west' , 'West')
        ])
    active = fields.Boolean(default=True)
    image = fields.Image()
    state = fields.Selection([
        ('new' , 'New'),
        ('sold' , 'Sold'),
        ('cancel' , 'Cancel')], default = 'new')

    date_deadline = fields.Date()

    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user.partner_id.id)
    buyer_id = fields.Many2one('res.partner', default=lambda self: self.env.user.partner_id.id)


    def action_sold(self):
        for record in self:
            if record.state=="cancel":
                raise UserError("Property Can Not Sold")
            record.state="sold"

    def action_cancel(self):
        for record in self:
            if record.state=="sold":
                raise UserError("Property Can Be Not Cancel")
            record.state="cancel"

    