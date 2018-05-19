{
    'name': 'Product Barcode Label',
    'version': '1.1',
    'author': "Dirac ERP",
    'category': 'Product',
    'description': """
        Module allows to change the sequence of fields to display in barcode label report.
    """,
    'website': 'http://www.diracerp.in',
    
    'summary': 'Module allows to change the sequence of fields to display in barcode label report.',
    'depends': ['base', 'sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/small_barcode_label_view.xml',
        'barcode_label_report.xml',
        'views/product_barcode_report_template.xml',
    ],
   
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: