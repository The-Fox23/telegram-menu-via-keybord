"""Telegram keyboard rendering."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_CHAT_ID, CONF_MENUS, CONF_NOTIFY_ENTITY


class MenuManager:
    """Manage Telegram reply keyboards."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        self.hass = hass
        self.entry = entry

    @property
    def menus(self) -> dict[str, Any]:
        return self.entry.data.get(CONF_MENUS, {})

    @property
    def notify_entity(self) -> str:
        return self.entry.data[CONF_NOTIFY_ENTITY]

    @property
    def default_chat_id(self) -> str:
        return str(self.entry.data[CONF_CHAT_ID])

    async def show_menu(self, menu_name: str, chat_id: str | None = None) -> None:
        """Show a configured reply keyboard."""
        menu = self.menus.get(menu_name)
        if not isinstance(menu, dict):
            raise ValueError(f"Unknown Telegram menu: {menu_name}")

        keyboard = []
        for row in menu.get("rows", []):
            rendered_row = []
            for button in row:
                if isinstance(button, dict):
                    rendered_row.append(str(button.get("command", button.get("label", ""))))
                else:
                    rendered_row.append(str(button))
            keyboard.append(rendered_row)

        data = {
            "entity_id": self.notify_entity,
            "chat_id": [str(chat_id or self.default_chat_id)],
            "message": menu.get("message", "Bitte auswählen:"),
            "keyboard": keyboard,
        }

        await self.hass.services.async_call(
            "telegram_bot",
            "send_message",
            data,
            blocking=True,
        )

    async def hide_menu(self, chat_id: str | None = None) -> None:
        """Remove the Telegram reply keyboard."""
        data = {
            "entity_id": self.notify_entity,
            "chat_id": [str(chat_id or self.default_chat_id)],
            "message": "Tastatur ausgeblendet.",
            "keyboard": [["/hide_keyboard"]],
        }

        await self.hass.services.async_call(
            "telegram_bot",
            "send_message",
            data,
            blocking=True,
        )
