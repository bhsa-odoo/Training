from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers import portal

# # class MyController(http.Controller):
# #     @http.route('/estate/index', auth='public')
# #     def index(self,**kw):
# #         return "HELLO WORD"

class MyController(portal.CustomerPortal):
  
  
#     # @http.route('/estate/index', auth='public')
#     # def index(self,**kw):
#     #     return http.request.render('estate.index',{
#     #         'names':['abc','def','ghi']
#     #     })

    @http.route('/estate/property', auth='user', website=True)
    def index(self,**kw):
        estate=http.request.env['estate.property']
        return http.request.render('estate.index',{
            'properties':estate.search([])
        })


    def _prepare_home_portal_values(self,counters):
        values = super()._prepare_home_portal_values(counters)
        properties = request.env['estate.property']
        values['total_properties'] = properties.search_count([]) or 0
        return values

    @http.route('/my/properties', auth='user', website=True)
    def my_properties(self, **kw):
        estate = request.env['estate.property'].search([])
        values = self._prepare_portal_layout_values()
        values.update({
           'properties':estate, 
        })

        return http.request.render('estate.portal_my_properties',values)





# # class ../mymodule/estate(http.Controller):
# #     @http.route('/../mymodule/estate/../mymodule/estate', auth='public')
# #     def index(self, **kw):
# #         return "Hello, world"

# #     @http.route('/../mymodule/estate/../mymodule/estate/objects', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('../mymodule/estate.listing', {
# #             'root': '/../mymodule/estate/../mymodule/estate',
# #             'objects': http.request.env['../mymodule/estate.../mymodule/estate'].search([]),
# #         })

# #     @http.route('/../mymodule/estate/../mymodule/estate/objects/<model("../mymodule/estate.../mymodule/estate"):obj>', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('../mymodule/estate.object', {
# #             'object': obj
# #         })
