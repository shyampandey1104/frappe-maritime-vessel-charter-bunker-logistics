# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "maritime_bunker_charter"
app_title = "Frappe Maritime Vessel Charter Bunker Logistics"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Maritime Vessel Charter Bunker Logistics - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/maritime_bunker_charter/css/maritime_bunker_charter.bundle.css"
app_include_js = "/assets/maritime_bunker_charter/js/maritime_bunker_charter.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Maritime Vessel Charter Bunker Logistics Entry": {
        "validate": "maritime_bunker_charter.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "maritime_bunker_charter.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "maritime_bunker_charter.tasks.hourly_sync"
    ],
    "daily": [
        "maritime_bunker_charter.tasks.daily_reconciliation"
    ],
    "weekly": [
        "maritime_bunker_charter.tasks.weekly_digest"
    ]
}
