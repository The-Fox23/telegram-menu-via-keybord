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
alias: Telegram - Tastatur anzeigen
description: Zeigt die Telegram-Tastatur an
triggers:
  - trigger: event
    event_type: telegram_command
    event_data:
      command: /tastatur
  conditions: []
actions:
  - action: telegram_bot.send_message
    data:
      chat_id:
        - xxxxxxxxx
      message: '🏠 Bitte Funktion auswählen:'
      keyboard:
        - ' /Garage_Gross, /Garage_Klein'
        - ' /Balkon_auf, /Terrasse_auf'
        - ' /Haustuer, /spare'
      entity_id:
        - notify.telegram_bot_xxxxxxxxx_chat id
      parse_mode: html
mode: single

```

can only continue to work unchanged when the Reply Keyboard button itself contains `/Haustuer`.

For this reason, the integration deliberately keeps the configured `command` as the visible text for a **Reply Keyboard**.

Example:

```yaml
alias: Telegram - Aktion bei Tastendruck
description: Reagiert auf den Tastendruck und führt je nach Befehl eine Aktion aus
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
conditions: []
actions:
  - choose:
      - conditions:
          - condition: trigger
            id: haustuer
        sequence:
          - action: homematicip_local.switch_set_on_time
            target:
              entity_id: switch.hm_lc_sw4_wm_neq1635462_ch2
            data:
              on_time: 1
          - action: telegram_bot.send_message
            data:
              chat_id:
                - xxxxxxxx
              message: 🚪 Haustür-Aktion erfolgreich ausgeführt!
      - conditions:
          - condition: trigger
            id: garage_gross
        sequence:
          - action: homematicip_local.switch_set_on_time
            target:
              entity_id: switch.hm_lc_sw4_wm_neq1635462_ch1
            data:
              on_time: 1
          - action: telegram_bot.send_message
            data:
              chat_id:
                - xxxxxxx
              message: 🚗 Garage Groß wurde ausgelöst!
      - conditions:
          - condition: trigger
            id: garage_klein
        sequence:
          - action: homematicip_local.switch_set_on_time
            target:
              entity_id: switch.4_fachaktor_garage_klein_ch1
            data:
              on_time: 1
          - action: telegram_bot.send_message
            data:
              chat_id:
                - xxxxxxxxx
              message: 🚗 Garage Klein wurde ausgelöst!
mode: single
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
https://github.com/The-Fox23/telegram-menu-via-keyboard
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
