"""Config flow for Telegram Menu."""
from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector

from .const import CONF_CHAT_ID, CONF_MENUS, CONF_NOTIFY_ENTITY, DOMAIN

MAX_BUTTONS = 30


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the Telegram Menu config flow."""

    VERSION = 3

    def __init__(self) -> None:
        """Initialize the flow."""
        self._notify_entity = ""
        self._chat_id = ""
        self._menu_name = "main"
        self._message = "🏠 Bitte Funktion auswählen:"
        self._keyboard_type = "reply"
        self._buttons: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Configure the Telegram connection."""
        if user_input is not None:
            self._notify_entity = user_input[CONF_NOTIFY_ENTITY]
            self._chat_id = str(user_input[CONF_CHAT_ID])
            return await self.async_step_menu()

        schema = vol.Schema(
            {
                vol.Required(CONF_NOTIFY_ENTITY): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="notify")
                ),
                vol.Required(CONF_CHAT_ID): str,
            }
        )
        return self.async_show_form(step_id="user", data_schema=schema)

    async def async_step_menu(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Configure the menu itself."""
        if user_input is not None:
            self._menu_name = user_input["menu_name"].strip() or "main"
            self._message = user_input["message"].strip() or "Bitte auswählen:"
            self._keyboard_type = user_input["keyboard_type"]
            return await self.async_step_button()

        schema = vol.Schema(
            {
                vol.Required("menu_name", default=self._menu_name): str,
                vol.Required("message", default=self._message): str,
                vol.Required("keyboard_type", default=self._keyboard_type): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=[
                            selector.SelectOptionDict(value="reply", label="Normale Telegram-Tastatur"),
                            selector.SelectOptionDict(value="inline", label="Inline-Tastatur"),
                        ],
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                ),
            }
        )
        return self.async_show_form(step_id="menu", data_schema=schema)

    async def async_step_button(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Add one button at a time to the menu."""
        errors: dict[str, str] = {}

        if user_input is not None:
            label = user_input["label"].strip()
            command = user_input["command"].strip()
            row = int(user_input["row"])

            if not label:
                errors["label"] = "invalid_button"
            elif not command.startswith("/"):
                errors["command"] = "invalid_command"
            elif any(
                button["command"] == command for button in self._buttons
            ):
                errors["command"] = "duplicate_command"
            else:
                self._buttons.append(
                    {"label": label, "command": command, "row": row}
                )
                if len(self._buttons) >= MAX_BUTTONS:
                    return self._finish_entry()
                if user_input["add_another"]:
                    return await self.async_step_button()
                return self._finish_entry()

        schema = vol.Schema(
            {
                vol.Required("label"): str,
                vol.Required("command"): str,
                vol.Required("row", default=1): selector.NumberSelector(
                    selector.NumberSelectorConfig(
                        min=1,
                        max=10,
                        step=1,
                        mode=selector.NumberSelectorMode.BOX,
                    )
                ),
                vol.Required("add_another", default=False): selector.BooleanSelector(),
            }
        )
        return self.async_show_form(
            step_id="button",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "button_number": str(len(self._buttons) + 1),
                "max_buttons": str(MAX_BUTTONS),
                "keyboard_type": (
                    "Normale Telegram-Tastatur"
                    if self._keyboard_type == "reply"
                    else "Inline-Tastatur"
                ),
            },
        )

    def _finish_entry(self) -> config_entries.ConfigFlowResult:
        """Create the config entry from the menu editor."""
        rows: dict[int, list[dict[str, str]]] = {}
        for button in self._buttons:
            rows.setdefault(button["row"], []).append(
                {"label": button["label"], "command": button["command"]}
            )

        menu = {
            "message": self._message,
            "keyboard_type": self._keyboard_type,
            "rows": [rows[row] for row in sorted(rows)],
        }
        menus = {self._menu_name: menu}

        return self.async_create_entry(
            title=f"Telegram Menu – {self._menu_name}",
            data={
                CONF_NOTIFY_ENTITY: self._notify_entity,
                CONF_CHAT_ID: self._chat_id,
                CONF_MENUS: menus,
            },
        )
