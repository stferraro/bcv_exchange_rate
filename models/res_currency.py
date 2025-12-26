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
            This method is called to ensure that the USD and EUR rates are updated daily.
            It checks if the rate for today already exists, and if not, it creates a new rate entry.
            If the rate cannot be fetched, it logs a warning.
        """

        date = fields.Date.today()
        company = self.env.company

        usd_rate, eur_rate, rate_date = ExchangeRate.get_rates()

        usd_currency = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if usd_currency and usd_rate:
            existing = self.env['res.currency.rate'].search([
                ('currency_id', '=', usd_currency.id),
                ('company_id', '=', company.id),
                ('name', '=', date)
            ], limit=1)
            if not existing:
                self.env['res.currency.rate'].create({
                    'currency_id': usd_currency.id,
                    'company_rate': 1 / usd_rate if usd_rate else 0.0,
                    'name': date,
                    'company_id': company.id,
                })
                _logger.info("Rate created: USD = %s en %s", usd_rate, date)

        eur_currency = self.env['res.currency'].search([('name', '=', 'EUR')], limit=1)
        if eur_currency and eur_rate:
            existing = self.env['res.currency.rate'].search([
                ('currency_id', '=', eur_currency.id),
                ('company_id', '=', company.id),
                ('name', '=', date)
            ], limit=1)
            if not existing:
                self.env['res.currency.rate'].create({
                    'currency_id': eur_currency.id,
                    'company_rate': 1 / eur_rate if eur_rate else 0.0,
                    'name': date,
                    'company_id': company.id,
                })
                _logger.info("Rate created: EUR = %s en %s", eur_rate, date)