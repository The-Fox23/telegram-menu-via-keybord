"""Telegram Menu Home Assistant sidebar panel."""
from __future__ import annotations

from homeassistant.components import panel_custom
from homeassistant.components.frontend import async_remove_panel
from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PANEL_URL = f"/api/{DOMAIN}/panel.js"
PANEL_FRONTEND_URL_PATH = "telegram_menu"
PANEL_NAME = "telegram-menu-panel"
PANEL_ICON = "mdi:telegram"


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the Telegram Menu sidebar panel."""
    panel_path = hass.config.path("custom_components", DOMAIN, "panel.js")

    await hass.http.async_register_static_paths(
        [StaticPathConfig(PANEL_URL, panel_path, True)]
    )

    await panel_custom.async_register_panel(
        hass=hass,
        webcomponent_name=PANEL_NAME,
        frontend_url_path=PANEL_FRONTEND_URL_PATH,
        sidebar_title="Telegram Menu",
        sidebar_icon=PANEL_ICON,
        module_url=PANEL_URL,
        embed_iframe=False,
        require_admin=True,
    )


def async_unregister_panel(hass: HomeAssistant) -> None:
    """Remove the Telegram Menu sidebar panel."""
    async_remove_panel(hass, PANEL_FRONTEND_URL_PATH, warn_if_unknown=False)
