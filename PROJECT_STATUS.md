# Telegram Menu via Keyboard – Projektstatus

> Zentrale Projektdokumentation für die Weiterentwicklung der Home-Assistant-Integration **Telegram Menu via Keyboard**. Diese Datei wird bei größeren Entwicklungsschritten aktualisiert, damit der Projektstand auch in einer späteren Unterhaltung schnell wiederhergestellt werden kann.

## 1. Repository
- GitHub Repository: `The-Fox23/telegram-menu-via-keybord`
- Geplanter Zielname: `telegram-menu-via-keyboard`
- Integration Domain: `telegram_menu`
- Anzeigename: **Telegram Menu via Keyboard**
- Aktuelle Version: **0.5.0**
- Home Assistant Mindestversion laut `hacs.json`: **2026.1.0**
- Abhängigkeit: `telegram_bot`
- Integrationstyp: `service`
- IoT-Klasse: `local_push`
- `single_config_entry: true`

## 2. Projektziel
Die Integration soll Telegram in Home Assistant um eine komfortable grafische Menü- und Steuerungsoberfläche erweitern.

Langfristig soll **für jeden Telegram-Button keine separate Home-Assistant-Automation mehr nötig sein**. Stattdessen sollen Benutzer in einem grafischen Editor:
1. Menüs anlegen und bearbeiten.
2. Telegram-Buttons anlegen und bearbeiten.
3. Buttons anordnen.
4. Jedem Button direkt Home-Assistant-Aktionen zuweisen.
5. Mehrere Aktionen pro Button definieren können.
6. Diese Aktionen beim Empfang des Telegram-Befehls ausführen lassen.
7. Später optional Untermenüs und Bedingungen konfigurieren.

Das Bedienkonzept orientiert sich grundsätzlich an der Idee von **Switch Manager**: grafische Konfiguration direkt in Home Assistant und möglichst Nutzung des vorhandenen Home-Assistant-Action-Editors.

## 3. Architektur
### Aktuell
Telegram → Button/Command → Telegram Event → eigene Automation → Aktion

### Ziel
Telegram → Button/Command → Telegram Menu Integration → gespeicherte Button-Aktionen → Home Assistant

Damit soll für normale Button-Aktionen keine separate Automation mehr erforderlich sein.

## 4. Aktueller Funktionsstand
Die bestehende Integration kann:
- vorhandene Telegram-Notify-Entity verwenden
- Standard-Chat-ID speichern
- Menüs konfigurieren
- Telegram Reply Keyboards anzeigen
- Telegram Inline Keyboards anzeigen
- `telegram_menu.show` verwenden
- `telegram_menu.hide` verwenden
- mehrere Buttons in Reihen konfigurieren
- Button-Labels und Telegram-Commands speichern
- bestehende Telegram-Command-Automationen weiterhin unterstützen

### Services
#### `telegram_menu.show`
Parameter:
- `entry_id`
- `menu`
- `chat_id`

#### `telegram_menu.hide`
Parameter:
- `entry_id`
- `chat_id`

## 5. Aktuelle Konfiguration
### Schritt 1 – Telegram-Verbindung
- Telegram Notify Entity
- Standard Chat ID

### Schritt 2 – Menü
- Menüname
- Nachricht über der Tastatur
- Tastaturtyp: Reply Keyboard oder Inline Keyboard

### Schritt 3 – Buttons
- Anzeigename
- Telegram-Befehl
- Reihe
- weiteren Button hinzufügen

Aktuell maximal 30 Buttons über den Config Flow.

## 6. Wichtige technische Dateien
Unter `custom_components/telegram_menu/`:
- `__init__.py`: Setup, Services, Config Entry, Migration auf Version 3, MenuManager; registriert jetzt auch das neue Sidebar-Panel
- `config_flow.py`: klassischer Einrichtungs-/Menü-/Button-Flow
- `menu.py`: Menüverwaltung und Telegram-Tastaturdarstellung
- `const.py`: Integrationskonstanten
- `services.yaml`: Dokumentation der Services
- `strings.json`: Config-Flow-Texte
- `translations/de.json`: deutsche Übersetzungen
- `panel.py`: Registrierung des neuen Home-Assistant-Sidebar-Panels
- `panel.js`: erste grafische Panel-Oberfläche

Der bestehende Config Flow wird **zunächst nicht entfernt**. Er bleibt parallel zum neuen grafischen Editor bestehen, bis dieser stabil funktioniert.

## 7. HACS / Repository
- `manifest.json` verwendet den Namen **Telegram Menu via Keyboard**
- `hacs.json` wurde ebenfalls auf **Telegram Menu via Keyboard** angepasst
- Integrations-Icon vorhanden unter `custom_components/telegram_menu/brand/icon.png`
- Ein zusätzliches `logo.png` ist aktuell nicht erforderlich.
- README wurde auf das Projekt angepasst.
- README-Beispiele verwenden absichtlich Platzhalter wie `xxxxxxxx` für persönliche Telegram IDs/Entities. Diese Platzhalter sollen beibehalten werden.

## 8. Wichtige Entwicklungsentscheidung
Die aktuelle Telegram-Anbindung funktioniert. Deshalb wird der neue grafische Editor **schrittweise parallel zur bestehenden Funktionalität** entwickelt.

Zunächst werden nicht unnötig entfernt:
- bestehender Config Flow
- bestehende Services
- bestehende Menülogik

Erst wenn der neue Editor stabil funktioniert, wird entschieden, welche alten Funktionen noch benötigt werden.

## 9. Entwicklungsplan
### Schritt 1 – Grafisches Home-Assistant-Panel
Ziel:
- eigenes **Telegram Menu** Panel in der Home-Assistant-Seitenleiste
- vorhandene Menüs anzeigen
- vorhandene Buttons anzeigen

**Aktueller Stand:** Das Panel-Grundgerüst wurde in Version **0.5.0** angelegt und über `__init__.py` registriert. Die erste Oberfläche zeigt zunächst einen Status-/Platzhalterbereich. Die Anzeige der vorhandenen Menüs und Buttons folgt als nächster Teil dieses Schrittes.

**Status: IN ARBEIT – BITTE TESTEN**

### Schritt 2 – Menü-Editor
- Menü erstellen
- Menü umbenennen
- Menü löschen
- Menü-Nachricht bearbeiten
- Tastaturtyp auswählen

**Status: GEPLANT**

### Schritt 3 – Button-Editor
- Anzeigename
- Telegram Command
- Position/Reihe
- optional Icon
- bearbeiten
- löschen
- neuen Button hinzufügen

**Status: GEPLANT**

### Schritt 4 – Aktionen direkt am Button
Jeder Button erhält einen Action-Bereich. Möglichst soll der native Home-Assistant-Action-Editor verwendet werden.

**Status: GEPLANT**

### Schritt 5 – Aktionen ohne zusätzliche Automation
Bei z. B. `/Haustuer` soll die Integration den Button finden, dessen gespeicherte Aktionen laden und diese in Home Assistant ausführen.

**Status: GEPLANT**

### Schritt 6 – Mehrere Aktionen
Beispiel:
- Garage öffnen
- 1 Sekunde warten
- Licht einschalten
- Telegram-Nachricht senden

**Status: GEPLANT**

### Schritt 7 – Untermenüs
Beispiel:
- Hauptmenü → Garage → Garage groß / Garage klein / Zurück

**Status: GEPLANT**

### Schritt 8 – Bedingungen
Optional später:
- Wenn Alarmanlage deaktiviert → Haustür öffnen
- Sonst → Telegram-Nachricht

**Status: SPÄTER / OPTIONAL**

## 10. Teststrategie
Die Entwicklung erfolgt gemeinsam mit dem Benutzer.

Nach jeder größeren Änderung:
1. Repository aktualisieren.
2. Home Assistant neu starten bzw. Integration neu laden.
3. Funktion testen.
4. Ergebnis zurückmelden.
5. Fehler oder Verbesserung dokumentieren.
6. Erst danach nächsten Entwicklungsschritt beginnen.

Besonders relevant sind Rückmeldungen zu:
- Funktion
- Fehlern/Logmeldungen
- Desktop-Darstellung
- Smartphone-Darstellung
- Bedienbarkeit
- gewünschten Änderungen

## 11. Entwicklungsprinzipien
- Kleine Änderungen statt großer Komplettumbauten.
- Funktionierende Bestandteile möglichst erhalten.
- Nach jedem größeren Schritt testen.
- Keine unnötigen YAML-Automationen für Button-Aktionen.
- Bedienung möglichst nativ und Home-Assistant-typisch gestalten.
- Vorhandene Home-Assistant-UI-Komponenten nach Möglichkeit wiederverwenden.
- Keine persönlichen Telegram IDs, Tokens oder Zugangsdaten ins Repository.
- README und PROJECT_STATUS.md bei wichtigen Änderungen aktuell halten.
- Vor größeren Änderungen zuerst den aktuellen Repository-Stand prüfen.

## 12. Aktueller nächster Schritt
**Schritt 1 – grafisches Home-Assistant-Panel testen und anschließend die vorhandenen Menüs und Buttons aus der Config Entry in der Oberfläche anzeigen.**

Noch nicht Teil des ersten Schrittes:
- Button-Aktionen
- Action Editor
- automatische Aktionsausführung
- Bedingungen
- komplexe Untermenüs
- Entfernung des bisherigen Config Flows

## 13. Projektstatus
| Bereich | Status |
|---|---|
| Telegram Bot Anbindung | Funktioniert |
| Reply Keyboard | Funktioniert |
| Inline Keyboard | Funktioniert |
| `telegram_menu.show` | Funktioniert |
| `telegram_menu.hide` | Funktioniert |
| HACS Metadaten | Angepasst |
| Integration Icon | Vorhanden |
| Klassischer Config Flow | Funktioniert |
| Grafisches Panel – Grundgerüst | **Neu in 0.5.0 – zu testen** |
| Grafischer Editor | Noch nicht umgesetzt |
| Eigenes HA Panel | **In Arbeit** |
| Button-Aktionen ohne Automation | Geplant |
| Native HA Action Editor Integration | Geplant |
| Mehrere Aktionen | Geplant |
| Untermenüs | Geplant |
| Bedingungen | Optional / später |

## 14. Arbeitsweise bei zukünftigen Unterhaltungen
Bei einer späteren Fortsetzung dieses Projekts soll diese Datei zuerst als Projektstatus verwendet werden.

Danach werden die relevanten Dateien im Repository erneut geprüft, bevor Änderungen vorgenommen werden.

**Letzte Aktualisierung:** 2026-09-25

**Aktueller Fokus:** Schritt 1 – grafisches Home-Assistant-Panel für Telegram Menu.
