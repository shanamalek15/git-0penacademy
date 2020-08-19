{
    'name': "Open Academy",

    'summary': """Manage trainings""",

    'description': """
        Open Academy module for managing trainings:
            - training courses
            - training sessions
            - attendees registration
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',

        'security/security.xml',
        'security/ir.model.access.csv',
        'view/openacademy.xml',
        'data/sequence_data.xml',
        'data/mail_template.xml',
        'report/reports.xml',
        'report/receipt_student.xml',
        'templates/websitetemplate.xml'


    ],
    'images':[],


    # only loaded in demonstration mode
    'demo': [
    ],



    # only loaded in demonstration mode
}
