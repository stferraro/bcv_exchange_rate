{
    'name': 'BCV Exchange Rate',
    'version': '19.0.1.0.0',
    'summary': '''
        This module retrieves and updates the official USD and EUR exchange rates published by the 
        Central Bank of Venezuela (BCV), allowing them to be used within Odoo for accounting and 
        financial operations. 
        ''',
    'category': 'Finance/Accounting',
    'author': 'Gerardo Alí Ferraro Schelijasch',
    'website': 'https://soltecferr.com',
    'license': 'OPL-1',
    'depends': [
        'base',
        'l10n_ve',
    ],
    'external_dependencies': {
        'python': ['requests', 'beautifulsoup4', 'urllib3'],
    },
    "data": [

        # cron
        'data/update_rates_ve.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bcv_exchange_rate/static/src/js/currency_rate.js',
            'bcv_exchange_rate/static/src/xml/currency_rate.xml',
        ],
    },
    'installable': True,
    'application': True,
}
