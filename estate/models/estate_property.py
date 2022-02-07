from odoo import models,fields,api
from odoo.exceptions import UserError ,ValidationError

# Many2One

class EstatePropertyType(models.Model):
    _name='estate.property.type'
    _description='Estate Property Type'

    name=fields.Char()

    # Constraints
    _sql_constraints=[('unique_property_type_name', 'unique(name)', 'Type Can Not Duplicated')]

# Many2many  

class EstatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description='Estate Property Tag'

    name=fields.Char()

    # Constraints
    _sql_constraints=[('unique_property_tag_name','unique(name)', 'Tag Can Not Duplicated')]


 # One2Many   

class EstatePropertyOffer(models.Model):
    _name='estate.property.offer'
    _description='Estate Property Offer'

    price =fields.Float()
    status=fields.Selection([('accepted','Accepted'),('refuse','Refused')])
    partner_id=fields.Many2one('res.partner')
    property_id=fields.Many2one('estate.property')


    

# Accept and Refused


    def action_accepted(self):
        for record in self:
            record.status="accepted"

            #set Buyer and Selling price
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id



    def action_refused(self):
        for record in self:
            record.status="refuse"

 




class Buyer_Partner(models.Model) :
    _inherit = 'res.partner'

    is_buyer = fields.Boolean(domain = "[('is_buyer' , '=' , ['True'])]")

    
# Create Model

class Real_EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate_property"

    # Constraints Exeption Error

    _sql_constraints=[('positive_price', 'check(expected_price >= 0)', 'Enter Positive Value')]


    name = fields.Char(string="Property Name",default="Unknown",required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(default=lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2 ,readonly=True)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area =fields.Integer()
    garden_orientation =fields.Selection([
        ('North', 'North'),
        ('South','South'),
        ('East','East'),
        ('West','West')
         ])
    active=fields.Boolean(default=True)
    property_type_id=fields.Many2one('estate.property.type')
    salesman_id=fields.Many2one('res.users')
    buyer_id=fields.Many2one('res.partner')
    property_tag_ids=fields.Many2many('estate.property.tag')
    property_offer_ids=fields.One2many('estate.property.offer','property_id')
    total_area=fields.Integer(compute="_compute_area",inverse="_inverse_area")
    best_price=fields.Float(compute="_compute_best_price")
    validity=fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    state=fields.Selection([('new','New'),('sold','Sold'),('cancel','Cancelled')],default='new')


    def open_offers(self):
        view_id_all = self.env.ref('estate.estate_properties_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_all, 'tree']],
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }

    def open_confirm_offers(self):
        view_id_accept = self.env.ref('estate.estate_properties_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_accept, 'tree']],
            "domain": [('property_id', '=', self.id),('status','=','accepted')]
            } 


    # Onchange

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'South'
            else:
                record.garden_area=0
                record.garden_orientation = None

    # Compute Fields

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability,days=record.validity)

    @api.depends('property_offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            max_price=0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price=offer.price
            record.best_price=max_price        


    @api.depends('living_area','garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # inverse

    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    # Action Method Sold and Calcel 

    def action_sold(self):
        for record in self:
            if record.state=="cancel": 
                raise UserError(" Property Can NOt Sold")
            record.state="sold"

    def action_cancel(self):
        for record in self:
            if record.state=="sold":
                raise UserError("Property Can Be Not Cancel")
            record.state="cancel"

    
    # Constraints Validation Error

    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden Can Not Biggest Than The Living Area")

