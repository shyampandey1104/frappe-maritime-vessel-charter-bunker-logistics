# Frappe Maritime Shipping, Vessel Charter & Bunker Fuel Engine

[![Frappe Framework](https://img.shields.io/badge/Frappe-v15.x-blue.svg)](https://frappeframework.com/)
[![IMO 2020](https://img.shields.io/badge/IMO-MARPOL%20Annex%20VI-navy.svg)]()
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 📌 Executive Overview & Real-World Client Problem

Global ocean bulk and container shipping operates under rigid **Charter Party Agreements (BIMCO standard contracts)**. Shipowners and commercial charterers lose millions in commercial disputes:
1. **Laytime & Demurrage Disputes:** At destination discharge ports, vessel waiting times and port congestion trigger severe disputes over whether time counts under **SHINC** (Sundays & Holidays Included) or **SHEX** (Sundays & Holidays Excluded) clauses.
2. **Bunker Fuel Compliance Traps:** Under the **IMO 2020 MARPOL Annex VI regulations**, marine fuels (VLSFO) must not exceed 0.50% sulphur content. Burning non-compliant fuel triggers immediate port authority vessel detentions and fines.
3. **Voyage P&L Disconnect:** Charter hire calculations, bunker consumption per nautical mile, and port disbursements often exist in fragmented spreadsheets, obscuring true voyage profitability.

This Frappe application unifies vessel charter party contracts, automated laytime demurrage/despatch computation, and bunker fuel consumption tracking.

---

## 🏛️ System Architecture Flow

```mermaid
flowchart TD
    A["Charter Party Fixture (BIMCO Contract)"] -->|Daily Hire & Demurrage Rates| B["Voyage Management System"]
    B -->|Vessel Port Arrival (Notice of Readiness - NOR)| C["Statement of Facts (SoF)"]
    C -->|Laytime Calculation Engine| D{"Allowed Laytime vs Actual Hours"}
    D -->|Actual > Allowed| E["Demurrage Incurred (Invoice to Charterer)"]
    D -->|Actual < Allowed| F["Despatch Earned (Credit to Charterer)"]
    G["Noon Reports / Engine Telemetry"] -->|Daily Consumption MT| H["Bunker Fuel Ledger (VLSFO / LSMGO)"]
    H -->|Sulphur Verification <= 0.50%| I["IMO 2020 Environmental Compliance Pass"]
    E & F & H --> J["Consolidated Voyage P&L Statement"]
```

---

## 🚀 Key Engineering Capabilities

- **Automated Laytime Demurrage Calculator:** Takes Notice of Readiness (NOR) and Statement of Facts (SoF) event timestamps, computes exact demurrage/despatch amounts in USD.
- **IMO 2020 Bunker Fuel Verifier:** Tracks bunker delivery notes (BDN), bunker stock on board (ROB), and enforces the 0.50% m/m sulphur ceiling.
- **Charter Party Financial Ledger:** Computes daily hire pro-rata, port agency disbursements, and off-hire downtime deductions.
- **Voyage Performance Analytics:** Analyzes weather routing impact, fuel economy curves, and speed-consumption warranty compliance.

---

## 📂 Frappe DocType Schema & Data Structure

```text
maritime_bunker_charter/
├── maritime_bunker_charter_core/
│   ├── doctype/
│   │   ├── charter_party_voyage/
│   │   │   ├── charter_party_voyage.json
│   │   │   ├── charter_party_voyage.py
│   │   │   └── charter_party_voyage.js
│   │   └── bunker_consumption_log/
│   │       └── bunker_consumption_log.json
│   └── workspace/
│       └── maritime_bunker_charter_workspace/
│           └── maritime_bunker_charter_workspace.json
```

---

## ⚡ Frappe Hooks & Whitelisted APIs

- **REST Endpoint:** `POST /api/method/maritime_bunker_charter.api.calculate_laytime_demurrage`
- **Whitelisted Method:** `@frappe.whitelist() def record_bunker_consumption(voyage_id, fuel_grade, beginning_stock_mt, fuel_consumed_mt, sulphur_content_pct)`
- **Hooks Event:** `on_submit` of `charter_party_voyage` triggers automatic billing entries in Accounts Receivable.

---

## 🛠️ Installation & Bench Setup

```bash
bench get-app https://github.com/shyampandey1104/frappe-maritime-vessel-charter-bunker-logistics
bench --site erp.yourdomain.com install-app maritime_bunker_charter
bench --site erp.yourdomain.com migrate
python3 -m unittest discover tests
```

---

## 📄 License
MIT License. Tailored for Shipowners, Charterers, Marine Logistics Operators, and Bunker Traders.
