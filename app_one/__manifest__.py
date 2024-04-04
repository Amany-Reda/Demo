{
    'name' : 'App One66',
    'author' : 'Mohamed Ramadan',
    'category' : '',
    'version' : "16.0.0.1.0",
    'depends' : [
        'base', 'sale_management', 'account',
    ],
    'data' : [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/asset_view.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml',
        'views/asset_loan_view.xml',
        'views/category_group_view.xml',
        'views/sale_order_inherit.xml',
        'views/make_order_view.xml',
        'report/asset_report.xml',
        'report/asset_report_template.xml',

    ],
    'assets': {
        'web.assets_backend': ['app_one/static/src/css/property.css']
    },
    'application' : True,
}
