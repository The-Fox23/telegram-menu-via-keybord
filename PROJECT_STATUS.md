# Telegram Menu via Keyboard – Projektstatus

> Zentrale Projektdokumentation für die Weiterentwicklung der Home-Assistant-Integration **Telegram Menu via Keyboard**. Diese Datei wird bei größeren Entwicklungsschritten aktualisiert.

## 1. Repository
- GitHub Repository: `The-Fox23/telegram-menu-via-keybord`
- Geplanter Zielname: `telegram-menu-via-keyboard`
- Integration Domain: `telegram_menu`
- Anzeigename: **Telegram Menu via Keyboard**
- Aktuelle Version: **0.5.0**
- Home Assistant Mindestversion laut `hacs.json`: **2026.1.0**
- Abhängigkeiten: `telegram_bot`, `panel_custom`
- Integrationstyp: `service`
- IoT-Klasse: `local_push`
- `single_config_entry: true`

## 2. Projektziel
Die Integration soll Telegram in Home Assistant um eine komfortable grafische Menü- und Steuerungsoberfläche erweitern.

Langfristig soll für normale Telegram-Buttons **keine separate Home-Assistant-Automation** mehr nötig sein. Stattdessen sollen Menüs, Buttons und deren Aktionen direkt in der Integration konfiguriert werden.

## 3. Architektur
### Aktuell
Telegram → Button/Command → Telegram Event → eigene Automation → Aktion

### Ziel
Telegram → Button/Command → Telegram Menu Integration → gespeicherte Button-Aktionen → Home Assistant

## 4. Aktueller Funktionsstand
Die bestehende Integration kann:
- Telegram Notify Entity verwenden
- Standard-Chat-ID speichern
- Reply Keyboards anzeigen
- Inline Keyboards anzeigen
- `telegram_menu.show` verwenden
- `telegram_menu.hide` verwenden
- Buttons in Reihen konfigurieren
- Button-Labels und Telegram-Commands speichern
- bestehende Telegram-Command-Automationen unterstützen
- ein eigenes Home-Assistant-Sidebar-Panel bereitstellen
- das Sidebar-Icon **`mdi:keyboard`** anzeigen
- bestehende Menüs und Buttons grafisch laden
- Menüs grafisch erstellen, umbenennen und löschen
- Menü-Nachricht und Tastaturtyp grafisch ändern
- Buttons grafisch erstellen, bearbeiten und löschen
- Änderungen über die Home-Assistant-WebSocket-API speichern

## 5. Grafischer Editor
Das Panel bietet jetzt ausdrücklich:
- **+ Menü erstellen**
- **+ Erstes Menü erstellen**, wenn noch kein Menü vorhanden ist
- **+ Button erstellen** innerhalb eines Menüs
- Anzeigename des Buttons
- Telegram-Befehl
- Button löschen
- Menü-Nachricht
- Tastaturtyp
- Menü umbenennen/löschen
- **Speichern**

Home Assistant Custom Panels erhalten ihre Konfiguration über die `panel`-Property und `panel.config`; das Panel nutzt zusätzlich eine WebSocket-Verbindung, um die aktuelle Config Entry zu laden und zu speichern. citeturn0search0

## 6. Wichtige technische Dateien
Unter `custom_components/telegram_menu/`:
- `__init__.py`: Setup, Services, WebSocket-API und Config Entry
- `config_flow.py`: bisheriger klassischer Config Flow
- `menu.py`: Telegram-Menüausgabe
- `const.py`: Konstanten
- `panel.py`: Sidebar-Panel
- `panel.js`: grafischer Menü-/Button-Editor
- `PROJECT_STATUS.md`: Projektstatus

Der klassische Config Flow bleibt zunächst erhalten.

## 7. Entwicklungsplan
### Schritt 1 – Grafisches Home-Assistant-Panel
**Status: IMPLEMENTIERT / TESTEN**

### Schritt 2 – Menü-Editor
- Menü erstellen
- Menü umbenennen
- Menü löschen
- Nachricht bearbeiten
- Tastaturtyp auswählen

**Status: IMPLEMENTIERT / TESTEN**

### Schritt 3 – Button-Editor
- Button erstellen
- Anzeigename
- Telegram Command
- Position/Reihe
- bearbeiten
- löschen

**Status: IMPLEMENTIERT / TESTEN**

### Schritt 4 – Aktionen direkt am Button
Jeder Button soll einen eigenen Action-Bereich erhalten. Möglichst soll der native Home-Assistant-Action-Editor verwendet werden.

**Status: ALS NÄCHSTES**

### Schritt 5 – Aktionen ohne zusätzliche Automation
Telegram-Befehl → Button suchen → gespeicherte Aktionen ausführen.

**Status: GEPLANT**

### Schritt 6 – Mehrere Aktionen
Beispiel:
- Garage öffnen
- 1 Sekunde warten
- Licht einschalten
- Telegram-Nachricht senden

**Status: GEPLANT**

### Schritt 7 – Untermenüs
**Status: GEPLANT**

### Schritt 8 – Bedingungen
**Status: SPÄTER / OPTIONAL**

## 8. Aktueller Test
Der Benutzer hat bestätigt, dass das **Sidebar-Icon jetzt sichtbar ist**.

Als Nächstes soll geprüft werden:
1. Wird das Panel korrekt geladen?
2. Wird ein bestehendes Menü angezeigt?
3. Gibt es sichtbar die Schaltfläche **+ Menü erstellen**?
4. Kann ein Menü angelegt werden?
5. Erscheint darin **+ Button erstellen**?
6. Kann ein Button gespeichert werden?
7. Bleibt die Konfiguration nach Neustart erhalten?

Wenn das funktioniert, beginnt Schritt 4 mit den Button-Aktionen.

## 9. Bekannte offene Punkte
- Native Home-Assistant-Action-Editor-Integration fehlt noch.
- Button-Aktionen werden noch nicht ausgeführt.
- Mehrere Aktionen pro Button fehlen noch.
- Untermenüs fehlen noch.
- Bedingungen fehlen noch.

## 10. Entwicklungsprinzipien
- Funktionierende Telegram-Anbindung nicht unnötig verändern.
- Kleine, testbare Schritte.
- Nach größeren Änderungen `PROJECT_STATUS.md` aktualisieren.
- Keine persönlichen Telegram IDs, Tokens oder Zugangsdaten ins Repository.
- Bestehenden Config Flow zunächst erhalten.
- Home-Assistant-native UI nach Möglichkeit verwenden.

**Letzte Aktualisierung:** 2026-09-25

**Aktueller Fokus:** Menü-/Button-Erstellung testen; danach Button-Aktionen integrieren.
