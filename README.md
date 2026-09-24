# Telegram Menu for Home Assistant

Custom Home Assistant integration for building reusable Telegram reply keyboards.

## Features

- `/commands` as Telegram reply-keyboard buttons
- Arbitrary button rows
- Submenus
- Home Assistant UI/config flow
- Uses your existing Home Assistant Telegram Bot integration
- Does **not** replace or modify `telegram_command` events
- Provides `telegram_menu.show` and `telegram_menu.hide` actions

## Important

This integration is a menu/keyboard layer. Your existing Telegram command automations remain responsible for what `/Haustuer`, `/Garage_Gross`, etc. actually do.

### Example

A menu can be configured as:

```json
{
  "main": {
    "message": "🏠 Bitte Funktion auswählen:",
    "rows": [
      [
        {"label": "🚪 Haustür", "command": "/Haustuer"},
        {"label": "🚗 Garage Groß", "command": "/Garage_Gross"},
        {"label": "🚗 Garage Klein", "command": "/Garage_Klein"}
      ]
    ]
  }
}
```

The `command` value is what Telegram sends when the button is pressed. The current implementation renders the command itself as the button text; label/submenu rendering will be expanded in the next development step.


## Installation über HACS

## Benutzerdefiniertes Repository

Da dieses Projekt aktuell nicht Bestandteil des offiziellen HACS-Repository-Katalogs ist, muss es als benutzerdefiniertes Repository hinzugefügt werden.

1. HACS in Home Assistant öffnen
2. Oben rechts auf die **drei Punkte** klicken
3. **Benutzerdefinierte Repositories** auswählen
4. Folgendes Repository eintragen:

```text
https://github.com/The-Fox23/divera-hacs-custom-server](https://github.com/The-Fox23/telegram-menu-via-keybord
```

5. Kategorie:

```text
Integration
```

6. **Hinzufügen** auswählen
7. Nach **DIVERA 24/7 with Server URL** suchen
8. Integration herunterladen
9. Home Assistant vollständig neu starten


For HACS:

1. Create a GitHub repository from this project.
2. In HACS, add the repository as a custom repository.
3. Select category `Integration`.
4. Install `Telegram Menu`.
5. Restart Home Assistant.
6. Add **Telegram Menu** from Settings → Devices & services.

## Action example

```yaml
action:
  - action: telegram_menu.show
    data:
      menu: main
```

If more than one Telegram Menu config entry exists, specify its `entry_id`.

## Existing Telegram commands

Your existing automation can remain like:

```yaml
triggers:
  - trigger: event
    event_type: telegram_command
    event_data:
      command: /Haustuer
    id: haustuer

  - trigger: event
    event_type: telegram_command
    event_data:
      command: /Garage_Gross
    id: garage_gross

  - trigger: event
    event_type: telegram_command
    event_data:
      command: /Garage_Klein
    id: garage_klein
```

The Telegram Menu integration does not consume, replace or rename these commands.

## Roadmap

- Visual menu editor instead of JSON
- True label/command separation
- Submenu buttons with automatic menu navigation
- Back/Home buttons
- Optional resize/one-time keyboard settings
- Per-chat menus
- Menu visibility and authorization rules
- Tests and CI
