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
        'views/estate_property_views.xml',
    ],
    
    'installable': True,
    'application': True,
}