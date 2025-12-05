# NeoCognito Ecosystem & Workspace Context

This workspace manages the integrated Personal Knowledge Management (PKM) and Task Management ecosystem for user `lemondesk`. The system is currently evolving from a local-only setup to a distributed client-server architecture powered by a Raspberry Pi Zero 2W.

## 🧠 Core Projects

### 1. Neo-Cortex (In Development)
*   **Location:** `~/Neo-Cortex`
*   **Type:** Server / Backend
*   **Target Hardware:** Raspberry Pi Zero 2W (Headless).
*   **Purpose:** Acts as the "Brain" of the ecosystem. It ingests tasks and reminders, applies an intelligent prioritization algorithm (Eisenhower Matrix), and serves a visual "Wall" dashboard via HTTP/SSE.
*   **Planned Stack:** Python (FastAPI/Litestar), SQLite (WAL mode), HTMX, Alpine.js.
*   **Constraints:** Extreme resource efficiency (512MB RAM limit).

### 2. Reminder CLI
*   **Location:** `~/reminder-cli`
*   **Type:** Data Source / Client tool
*   **Purpose:** "Fire & Forget" CLI for scheduling notifications.
*   **Data Storage:** `~/.reminder_cli.json` (Local JSON).
*   **Future Integration:** A background watcher will sync this local file with the Neo-Cortex server.

### 3. NeoCognito (Legacy/Core)
*   **Location:** `~/Dev_Pro/NeoCognito`
*   **Type:** PKM / Visualization
*   **Purpose:** Manages the Markdown Vault (Zettelkasten/GTD) and desktop widgets (Conky).
*   **Data Storage:** `~/Vault` (00_Inbox.md, TODO_Today.md).
*   **Key Scripts:** `capture.sh` (Input), `launch_wall.sh` (Display), `neocognito-bot.service` (Telegram Bot).

## ⚙️ Infrastructure & Environment

### Host Machine (Desktop)
*   **OS:** Linux (Arch-based).
*   **IP:** `192.168.15.13/24`.
*   **Role:** Development station and primary input source (via CLI and Obsidian).

### Raspberry Pi Zero 2W (Target: `neocortex`)
*   **OS:** Raspberry Pi OS Lite (64-bit).
*   **Hostname:** `neocortex` (or `neocortex.local`).
*   **Network Constraints:**
    *   **Wi-Fi:** 2.4GHz Only (Cannot see 5GHz networks).
    *   **Setup:** Headless via `rpi-imager` or manual `bootfs` configuration.
*   **Current Status:** Troubleshooting network connectivity (Wi-Fi band mismatch or USB Gadget mode issues).

## 📂 Key Data Paths
*   **Reminders:** `~/.reminder_cli.json`
*   **Vault/Notes:** `~/Vault/`
*   **NeoCognito Config:** `~/Dev_Pro/NeoCognito/config/`

## 🛠 Development Guidelines
*   **Philosophy:** "The Hard Way" / Professional Engineering.
*   **Priorities:** Efficiency, Clean Architecture, Stability.
*   **Approach:** Iterate on the new `Neo-Cortex` system without breaking the existing, functional `reminder-cli` and `NeoCognito` tools. Use "Satellite" agents for integration rather than direct modification.
