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
        .container {
          max-width: 1100px;
          margin: 0 auto;
        }
        h1 { margin: 0 0 8px; font-size: 28px; }
        .subtitle {
          color: var(--secondary-text-color);
          margin-bottom: 24px;
        }
        .info {
          background: var(--card-background-color);
          border-radius: 12px;
          padding: 20px;
          box-shadow: var(--ha-box-shadow);
        }
      </style>
      <div class="container">
        <h1>Telegram Menu</h1>
        <div class="subtitle">Grafischer Menü-Editor</div>
        <div class="info">
          <strong>Schritt 1</strong>
          <p>Das Telegram-Menu-Panel ist installiert.</p>
          <p>Als Nächstes werden die vorhandenen Menüs und Buttons hier angezeigt.</p>
        </div>
      </div>
    `;
  }
}

if (!customElements.get("telegram-menu-panel")) {
  customElements.define("telegram-menu-panel", TelegramMenuPanel);
}
