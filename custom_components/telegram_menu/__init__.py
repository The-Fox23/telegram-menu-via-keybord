"""Telegram Menu integration for Home Assistant."""
from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv, entity_registry as er
import voluptuous as vol

from .const import CONF_CHAT_ID, CONF_NOTIFY_ENTITY, CONF_MENUS, DOMAIN
from .menu import MenuManager

PLATFORMS: list[str] = []


async def async_setup(hass: HomeAssistant, config: dict[str, Any]) -> bool:
    """Set up the Telegram Menu integration."""
    hass.data.setdefault(DOMAIN, {})

    async def handle_show(call: ServiceCall) -> None:
        """Show a configured Telegram menu."""
        entry_id = call.data.get("entry_id")
        menu = call.data.get("menu", "main")
        chat_id = call.data.get("chat_id")

        manager = _get_manager(hass, entry_id)
        await manager.show_menu(menu, chat_id)

    async def handle_hide(call: ServiceCall) -> None:
        """Hide the Telegram reply keyboard."""
        entry_id = call.data.get("entry_id")
        chat_id = call.data.get("chat_id")

        manager = _get_manager(hass, entry_id)
        await manager.hide_menu(chat_id)

    hass.services.async_register(
        DOMAIN,
        "show",
        handle_show,
        schema=vol.Schema(
            {
                vol.Optional("entry_id"): cv.string,
                vol.Optional("menu", default="main"): cv.string,
                vol.Optional("chat_id"): cv.string,
            }
        ),
    )

    hass.services.async_register(
        DOMAIN,
        "hide",
        handle_hide,
        schema=vol.Schema(
            {
                vol.Optional("entry_id"): cv.string,
                vol.Optional("chat_id"): cv.string,
            }
        ),
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a Telegram Menu config entry."""
    manager = MenuManager(hass, entry)
    hass.data[DOMAIN][entry.entry_id] = manager
    return True


async def async_migrate_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Migrate older Telegram Menu config entries."""
    if config_entry.version < 3:
        hass.config_entries.async_update_entry(
            config_entry,
            version=3,
        )
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Telegram Menu config entry."""
    hass.data[DOMAIN].pop(entry.entry_id, None)
    return True


def _get_manager(hass: HomeAssistant, entry_id: str | None) -> MenuManager:
    """Get a configured menu manager."""
    entries = hass.data[DOMAIN]
    if entry_id:
        manager = entries.get(entry_id)
        if manager is None:
            raise ValueError(f"Telegram Menu entry not found: {entry_id}")
        return manager
    if len(entries) == 1:
        return next(iter(entries.values()))
    if not entries:
        raise ValueError("No Telegram Menu configuration is loaded")
    raise ValueError("More than one Telegram Menu configuration exists; specify entry_id")
