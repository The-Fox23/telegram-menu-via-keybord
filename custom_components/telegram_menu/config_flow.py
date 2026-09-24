"""Config flow for Telegram Menu."""
from __future__ import annotations

import json
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import CONF_CHAT_ID, CONF_MENUS, CONF_NOTIFY_ENTITY, DOMAIN

DEFAULT_MENUS = {
    "main": {
        "message": "🏠 Bitte Funktion auswählen:",
        "keyboard_type": "reply",
        "rows": [
            [
                {"label": "🚪 Haustür", "command": "/Haustuer"},
                {"label": "🚗 Garage Groß", "command": "/Garage_Gross"},
                {"label": "🚗 Garage Klein", "command": "/Garage_Klein"},
            ]
        ],
    }
}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Configure the integration."""
        errors: dict[str, str] = {}

        if user_input:
            try:
                menus = json.loads(user_input[CONF_MENUS])
                _validate_menus(menus)
            except (json.JSONDecodeError, ValueError, TypeError):
                errors["base"] = "invalid_menus"
            else:
                data = {
                    CONF_NOTIFY_ENTITY: user_input[CONF_NOTIFY_ENTITY],
                    CONF_CHAT_ID: str(user_input[CONF_CHAT_ID]),
                    CONF_MENUS: menus,
                }
                return self.async_create_entry(
                    title="Telegram Menu",
                    data=data,
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_NOTIFY_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="notify")
                ),
                vol.Required(CONF_CHAT_ID): str,
                vol.Required(
                    CONF_MENUS,
                    default=json.dumps(DEFAULT_MENUS, ensure_ascii=False, indent=2),
                ): selector.TextSelector(
                    selector.TextSelectorConfig(multiline=True)
                ),
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)


def _validate_menus(menus: Any) -> None:
    """Validate the menu definition."""
    if not isinstance(menus, dict) or not menus:
        raise ValueError("menus must be a non-empty object")

    for name, menu in menus.items():
        if not isinstance(name, str) or not isinstance(menu, dict):
            raise ValueError("Each menu must be an object")

        keyboard_type = menu.get("keyboard_type", "reply")
        if keyboard_type not in {"reply", "inline"}:
            raise ValueError("keyboard_type must be 'reply' or 'inline'")

        if "rows" not in menu or not isinstance(menu["rows"], list):
            raise ValueError(f"Menu {name} must contain rows")

        for row in menu["rows"]:
            if not isinstance(row, list):
                raise ValueError("Each row must be a list")

            for button in row:
                if isinstance(button, str):
                    if not button.startswith("/"):
                        raise ValueError("Commands must start with /")
                    continue

                if not isinstance(button, dict):
                    raise ValueError("Buttons must be strings or objects")

                command = button.get("command")
                if not isinstance(command, str) or not command.startswith("/"):
                    raise ValueError("Button command must start with /")

                label = button.get("label")
                if label is not None and not isinstance(label, str):
                    raise ValueError("Button label must be a string")

                submenu = button.get("submenu")
                if submenu is not None and submenu not in menus:
                    raise ValueError(f"Unknown submenu: {submenu}")
