from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import requests
import logging
from bs4 import BeautifulSoup
from datetime import date

_logger = logging.getLogger(__name__)


class ExchangeRate:
    @staticmethod
    def get_rates():
        """
            Gets the exchange rate of the day from the BCV website.

            Returns:
                tuple: (float: USD rate, float: EUR rate, date: rate date)
        """
        disable_warnings(InsecureRequestWarning)
        bcv_url = "https://www.bcv.org.ve/"
        current_date = date.today()

        try:
            response = requests.get(bcv_url, verify=False, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            usd_container = soup.find(id="dolar")
            eur_container = soup.find(id="euro")

            if not usd_container or not eur_container:
                _logger.error("Could not find USD or EUR rate containers on BCV page.")
                return None

            usd_value = (
                usd_container.text.replace("\n", "").replace("USD", "").replace(",", ".").strip()
            )
            eur_value = (
                eur_container.text.replace("\n", "").replace("EUR", "").replace(",", ".").strip()
            )
            return float(usd_value), float(eur_value), current_date
        except Exception as e:
            _logger.exception("Failed to fetch exchange rates from BCV: %s", e, exc_info=True)
            return None