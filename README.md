# Telegram Menu for Home Assistant

Custom Home Assistant integration for managing Telegram menus on top of the official Home Assistant `telegram_bot` integration.

## What this integration does

- Uses the existing Home Assistant `telegram_bot` integration
- Does **not** replace or modify Telegram polling/webhooks
- Does **not** replace `telegram_command` events
- Supports normal Telegram **Reply Keyboards**
- Supports Telegram **Inline Keyboards**
- Allows multiple rows and buttons
- Provides `telegram_menu.show` and `telegram_menu.hide` actions

## Telegram Bot: Privacy Mode deaktivieren

Damit der Telegram Bot die Nachrichten bzw. Befehle aus einer normalen **Reply Keyboard** zuverlässig an Home Assistant weitergeben kann, muss bei deinem Bot in **BotFather** der **Privacy Mode** deaktiviert werden.

### Privacy Mode auf Disable stellen

1. Telegram öffnen und **@BotFather** aufrufen.
2. Den Befehl `/mybots` senden.
3. Deinen Home-Assistant-Telegram-Bot auswählen.
4. **Bot Settings** öffnen.
5. **Group Privacy** auswählen.
6. **Turn off** auswählen bzw. den Privacy Mode auf **Disable** stellen.
7. Danach den Bot in Home Assistant weiter wie gewohnt verwenden.

Die Einstellung ist besonders wichtig, wenn der Bot in einer **Telegram-Gruppe** verwendet wird. Bei aktiviertem Privacy Mode verarbeitet Telegram in Gruppen nur bestimmte Nachrichten und Befehle. Dadurch können Nachrichten aus der Reply Keyboard bzw. die erwarteten `telegram_command`-Events unter Umständen nicht bei Home Assistant ankommen.

**Empfehlung:** Stelle den Privacy Mode bereits vor dem ersten Test des Menüs auf **Disable**, damit die Fehlersuche nicht durch die Telegram-Bot-Einstellungen erschwert wird.

> Hinweis: Diese Einstellung wird in **BotFather** vorgenommen und nicht in dieser Home-Assistant-Integration. Die offizielle `telegram_bot`-Integration von Home Assistant bleibt unverändert.

## Important: Reply Keyboard compatibility

A normal Telegram Reply Keyboard sends the **visible button text** back to Telegram as a message.

That means an existing automation such as:

```yaml
triggers:
  - trigger: event
    event_type: telegram_command
    event_data:
      command: /Haustuer
```

can only continue to work unchanged when the Reply Keyboard button itself contains `/Haustuer`.

For this reason, the integration deliberately keeps the configured `command` as the visible text for a **Reply Keyboard**.

Example:

```json
{
  "main": {
    "message": "🏠 Bitte Funktion auswählen:",
    "keyboard_type": "reply",
    "rows": [
      [
        {"label": "🚪 Haustür", "command": "/Haustuer"},
        {"label": "🚗 Garage Groß", "command": "/Garage_Gross"}
      ]
    ]
  }
}
```

The `label` is stored for the menu definition, but a Reply Keyboard displays `command` so that existing `telegram_command` automations remain compatible.

## Inline Keyboard

Inline keyboards can use a separate friendly label and command/callback value:

```json
{
  "main": {
    "message": "🏠 Bitte Funktion auswählen:",
    "keyboard_type": "inline",
    "rows": [
      [
        {"label": "🚪 Haustür", "command": "/Haustuer"},
        {"label": "🚗 Garage Groß", "command": "/Garage_Gross"}
      ]
    ]
  }
}
```

The visible button text is the configured `label`.

**Note:** Inline keyboard callback handling will be expanded in a later development step. The current implementation prepares the inline keyboard structure while keeping the existing Telegram integration untouched.

## Configuration

The current config flow asks for:

1. The existing Telegram notify entity
2. A default Telegram chat ID
3. Menu definitions

The menu definition is currently entered as JSON. A visual menu editor is planned.

## Actions

Show a menu:

```yaml
action:
  - action: telegram_menu.show
    data:
      menu: main
```

Hide the Reply Keyboard:

```yaml
action:
  - action: telegram_menu.hide
```

If more than one Telegram Menu config entry exists, specify its `entry_id`.

## Existing Telegram automations remain usable

For Reply Keyboard commands, existing automations can remain unchanged:

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

The Telegram Menu integration does not consume, rename or replace these commands.

## HACS installation

This repository can be added as a custom HACS repository:

```
https://github.com/The-Fox23/telegram-menu-via-keybord
```

Select category **Integration**, install **Telegram Menu**, and restart Home Assistant.

## Roadmap

- Visual menu editor instead of JSON
- Submenu navigation
- Back/Home buttons
- Direct Home Assistant service actions
- Inline callback query handling
- Per-chat menus
- Menu visibility and authorization rules
- Tests and CI
