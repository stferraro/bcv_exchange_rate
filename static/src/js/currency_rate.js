/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { session } from "@web/session";

class CurrencyRate extends Component {
    setup() {
        super.setup(...arguments);
        this.state = useState({
            rate_usd: { rate: 0.0, symbol: "USD", currency_id: 0 },
            rate_eur: { rate: 0.0, symbol: "EUR", currency_id: 0 },
        });
        this.action = useService("action");
        this.orm = useService("orm");
        onWillStart(async () => {
            try {
                const rates = await this.orm.call(
                    "res.currency",
                    "exchange_rate_usd_eur",
                    [session.company_id]
                );

                if (rates) {
                    this.state.rate_usd = rates.usd;
                    this.state.rate_eur = rates.eur;
                }
            } catch (error) {
                console.error("Error fetching exchange rates:", error);
            }
        });
    }
    get rate_usd_display() {
        const { rate, symbol } = this.state.rate_usd;
        return `1$ = ${rate} Bs`;
    }
    get rate_eur_display() {
        const { rate, symbol } = this.state.rate_eur;
         return `1€ = ${rate} Bs`;
    }
    _openCurrencyUSD() {
        const { currency_id } = this.state.rate_usd;
        if (currency_id) {
            this.action.doAction({
                type: "ir.actions.act_window",
                name: "Currencies - USD",
                res_model: "res.currency",
                view_mode: "form",
                views: [[false, "form"]],
                res_id: currency_id,
                target: "new",
            });
        }
    }
    _openCurrencyEUR() {
        const { currency_id } = this.state.rate_eur;
        if (currency_id) {
            this.action.doAction({
                type: "ir.actions.act_window",
                name: "Currencies - EUR",
                res_model: "res.currency",
                view_mode: "form",
                views: [[false, "form"]],
                res_id: currency_id,
                target: "new",
            });
        }
    }
}
CurrencyRate.template = "CurrencyRate";
CurrencyRate.components = { Dropdown, DropdownItem };
export const currencyRate = { Component: CurrencyRate };
registry.category("systray").add("CurrencyRate", currencyRate, { sequence: 1 });
