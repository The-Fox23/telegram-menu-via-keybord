class TelegramMenuPanel extends HTMLElement {
  set hass(value) {
    this._hass = value;
    this._render();
  }

  connectedCallback() {
    this._render();
  }

  _render() {
    if (!this.isConnected) return;

    const menus = this._hass?.connection ? this._getMenus() : {};
    const menuEntries = Object.entries(menus);

    this.innerHTML = `
      <style>
        :host {
          display: block;
          box-sizing: border-box;
          padding: 24px;
          background: var(--primary-background-color);
          color: var(--primary-text-color);
          min-height: 100vh;
          font-family: var(--paper-font-body1_-_font-family, sans-serif);
        }
        .container { max-width: 1100px; margin: 0 auto; }
        h1 { margin: 0 0 4px; font-size: 28px; }
        .subtitle { color: var(--secondary-text-color); margin-bottom: 24px; }
        .menu {
          background: var(--card-background-color);
          border-radius: 12px;
          padding: 20px;
          margin-bottom: 20px;
          box-shadow: var(--ha-box-shadow);
        }
        .menu-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 8px;
        }
        .menu-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          border-radius: 10px;
          background: var(--primary-color);
          color: var(--text-primary-color, white);
          font-size: 20px;
        }
        .menu-title { font-size: 21px; font-weight: 600; }
        .message { color: var(--secondary-text-color); margin: 8px 0 18px; }
        .keyboard { display: flex; flex-direction: column; gap: 8px; }
        .row { display: flex; flex-wrap: wrap; gap: 8px; }
        .button {
          min-width: 160px;
          flex: 0 1 auto;
          border: 1px solid var(--divider-color);
          border-radius: 10px;
          padding: 12px 16px;
          background: var(--secondary-background-color);
        }
        .label { font-weight: 600; }
        .command {
          display: block;
          margin-top: 4px;
          color: var(--secondary-text-color);
          font-size: 13px;
        }
        .empty {
          background: var(--card-background-color);
          border-radius: 12px;
          padding: 24px;
          color: var(--secondary-text-color);
        }
      </style>
      <div class="container">
        <h1>Telegram Menu</h1>
        <div class="subtitle">Menüs und Buttons</div>
        <div id="content"></div>
      </div>
    `;

    const content = this.querySelector("#content");

    if (!menuEntries.length) {
      content.innerHTML = `
        <div class="empty">
          Noch keine Menüs konfiguriert.
        </div>
      `;
      return;
    }

    for (const [name, menu] of menuEntries) {
      const section = document.createElement("section");
      section.className = "menu";

      const header = document.createElement("div");
      header.className = "menu-header";
      header.innerHTML = '<div class="menu-icon">☰</div><div class="menu-title"></div>';
      header.querySelector(".menu-title").textContent = name;
      section.appendChild(header);

      if (menu?.message) {
        const message = document.createElement("div");
        message.className = "message";
        message.textContent = menu.message;
        section.appendChild(message);
      }

      const keyboard = document.createElement("div");
      keyboard.className = "keyboard";

      for (const row of menu?.rows || []) {
        const rowElement = document.createElement("div");
        rowElement.className = "row";

        for (const button of row || []) {
          const buttonElement = document.createElement("div");
          buttonElement.className = "button";

          const label = typeof button === "object"
            ? button.label || button.command
            : button;
          const command = typeof button === "object"
            ? button.command
            : button;

          const labelElement = document.createElement("span");
          labelElement.className = "label";
          labelElement.textContent = label || "Button";

          const commandElement = document.createElement("span");
          commandElement.className = "command";
          commandElement.textContent = command || "";

          buttonElement.append(labelElement, commandElement);
          rowElement.appendChild(buttonElement);
        }

        if (rowElement.childElementCount) keyboard.appendChild(rowElement);
      }

      section.appendChild(keyboard);
      content.appendChild(section);
    }
  }

  _getMenus() {
    // The first panel step receives the existing configuration through
    // Home Assistant panel configuration. This fallback keeps the panel
    // functional while the backend API is introduced in the next step.
    return this._panelConfig?.menus || {};
  }
}

if (!customElements.get("telegram-menu-panel")) {
  customElements.define("telegram-menu-panel", TelegramMenuPanel);
}
