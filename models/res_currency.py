from odoo import models, fields, api
from odoo.addons.bcv_exchange_rate.tools.exchange_rate import ExchangeRate
import logging

_logger = logging.getLogger(__name__)

class ResCurrency(models.Model):
    _inherit = 'res.currency'

    @api.model
    def _update_exchange_rates(self):
        """
        Obtain the USD and EUR exchange rates from BCV and update the currency rates.
        Checks if the rate for today already exists, and if not, creates a new rate entry.
        Logs warnings if the rates could not be fetched.
        """

        today = fields.Date.today()
        company = self.env.company

        rates = ExchangeRate.get_rates()
        if not rates:
            _logger.warning("Exchange rates were not updated due to BCV fetch errors.")
            return

        usd_rate, eur_rate, rate_date = rates

        usd_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if usd_currency and usd_rate:
            existing = self.env['res.currency.rate'].search([
                ('currency_id', '=', usd_currency.id),
                ('company_id', '=', company.id),
                ('name', '=', today)
            ], limit=1)
            if not existing:
                self.env['res.currency.rate'].create({
                    'currency_id': usd_currency.id,
                    'company_rate': 1 / usd_rate if usd_rate else 0.0,
                    'name': today,
                    'company_id': company.id,
                })
                _logger.info("Rate created: USD = %s on %s", usd_rate, today)

        eur_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
        if eur_currency and eur_rate:
            existing = self.env['res.currency.rate'].search([
                ('currency_id', '=', eur_currency.id),
                ('company_id', '=', company.id),
                ('name', '=', today)
            ], limit=1)
            if not existing:
                self.env['res.currency.rate'].create({
                    'currency_id': eur_currency.id,
                    'company_rate': 1 / eur_rate if eur_rate else 0.0,
                    'name': today,
                    'company_id': company.id,
                })
                _logger.info("Rate created: EUR = %s on %s", eur_rate, today)

    @api.model
    def exchange_rate_usd_eur(self, company_id=None):
        self._update_exchange_rates()

        today = fields.Date.today()
        usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        eur = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)

        usd_rate = self.env['res.currency.rate'].search([
            ('currency_id', '=', usd.id),
            ('name', '=', today)
        ], limit=1).inverse_company_rate if usd else 0.0

        eur_rate = self.env['res.currency.rate'].search([
            ('currency_id', '=', eur.id),
            ('name', '=', today)
        ], limit=1).inverse_company_rate if eur else 0.0

        usd_rate = round(usd_rate, 2)
        eur_rate = round(eur_rate, 2)

        return {
            'usd': {'rate': usd_rate, 'symbol': usd.symbol, 'currency_id': usd.id},
            'eur': {'rate': eur_rate, 'symbol': eur.symbol, 'currency_id': eur.id},
        }

