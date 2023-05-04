{
    'name': "estate",
    'version': '1.0',
    'author': 'Mohammad Faisal',
    'license': 'AGPL-3',
    'depends': ['base'],
    'category': 'Category',
    'summary': 'A module for managing real estate properties',
    'description': """
        Description text
    """,
    
    'data': [
        'data/ir.model.access.csv',
        "views/property_type_views.xml",
        "views/property_tag_views.xml",
        'views/estate_property_views.xml',
        "views/property_offer.xml",
        'views/estate_menus.xml',
    ],
    
    'installable': True,
    'application': True,
}