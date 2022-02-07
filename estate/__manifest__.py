{
    'name': 'Real_Estate',
    'version': '1.0',
    'category': 'Sales',
    'application': 'True',
    'depends':['base','account','website','portal'],
    'data':[
    		'security/ir.model.access.csv',
    		'views/estate_menus.xml',
            'views/estate_myproperty_menus.xml',


            'views/estate_property_views.xml',
            'views/estate_property_myproperty_views.xml',
            'views/estate_index.xml',
            'wizard/add_offer_views.xml',
            'views/estate_portal_view.xml',

    		
    ],

}
