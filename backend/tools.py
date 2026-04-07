"""
Tool implementations that Gemma 4 can call via native function calling.
All tools are designed to work fully offline (local DB, local data).
"""

from backend.db import query_protocols

REFERRAL_DATA = {
    "RED": {
        "action": "REFER URGENTLY — within 1 hour",
        "transport": "Arrange emergency transport immediately. Do not wait.",
        "stabilize": "Stabilize airway, breathing, circulation before transfer. Start IV access if trained.",
        "communicate": "Call ahead to receiving facility if radio/phone available.",
    },
    "YELLOW": {
        "action": "Refer within 24 hours",
        "transport": "Arrange transport for today or tomorrow. Patient can travel if stable.",
        "stabilize": "Monitor vitals every 30 minutes. Give first aid and document findings.",
        "communicate": "Write referral note with findings, actions taken, and timeline.",
    },
    "GREEN": {
        "action": "Manage locally. Follow up in 48-72 hours.",
        "transport": "No urgent transfer needed.",
        "stabilize": "Give appropriate first aid. Educate patient on warning signs.",
        "communicate": "Document in patient record. Advise patient when to return.",
    },
}

VITAL_THRESHOLDS = {
    "heart_rate": {"low": 50, "high_yellow": 100, "high_red": 120},
    "respiratory_rate": {"low": 10, "high_yellow": 25, "high_red": 30},
    "temperature_c": {"low": 35.5, "high_yellow": 38.0, "high_red": 40.0},
    "spo2": {"critical": 90, "warning": 94},
    "systolic_bp": {"low_red": 90, "low_yellow": 100, "high_yellow": 160, "high_red": 180},
}


def search_medical_protocols(query: str, category: str = "any") -> dict:
    """Search the local offline medical protocol database."""
    results = query_protocols(query, n_results=3)
    if category != "any":
        results = [r for r in results if r.get("category") == category] or results
    return {
        "protocols_found": len(results),
        "results": results,
    }


def assess_vital_signs(
    heart_rate: float = None,
    respiratory_rate: float = None,
    temperature_c: float = None,
    spo2: float = None,
    systolic_bp: float = None,
) -> dict:
    vitals = {k: v for k, v in {
        "heart_rate": heart_rate,
        "respiratory_rate": respiratory_rate,
        "temperature_c": temperature_c,
        "spo2": spo2,
        "systolic_bp": systolic_bp,
    }.items() if v is not None}
    return _assess_vital_signs_impl(vitals)


def _assess_vital_signs_impl(vitals: dict) -> dict:
    """
    Assess vital signs and return risk level.
    vitals: dict with optional keys: heart_rate, respiratory_rate,
            temperature_c, spo2, systolic_bp
    """
    flags = []
    level = "GREEN"

    hr = vitals.get("heart_rate")
    if hr is not None:
        if hr < VITAL_THRESHOLDS["heart_rate"]["low"] or hr > VITAL_THRESHOLDS["heart_rate"]["high_red"]:
            flags.append(f"Heart rate {hr} bpm — CRITICAL")
            level = "RED"
        elif hr > VITAL_THRESHOLDS["heart_rate"]["high_yellow"]:
            flags.append(f"Heart rate {hr} bpm — elevated")
            if level != "RED": level = "YELLOW"

    rr = vitals.get("respiratory_rate")
    if rr is not None:
        if rr < VITAL_THRESHOLDS["respiratory_rate"]["low"] or rr > VITAL_THRESHOLDS["respiratory_rate"]["high_red"]:
            flags.append(f"Respiratory rate {rr}/min — CRITICAL")
            level = "RED"
        elif rr > VITAL_THRESHOLDS["respiratory_rate"]["high_yellow"]:
            flags.append(f"Respiratory rate {rr}/min — elevated")
            if level != "RED": level = "YELLOW"

    temp = vitals.get("temperature_c")
    if temp is not None:
        if temp < VITAL_THRESHOLDS["temperature_c"]["low"] or temp >= VITAL_THRESHOLDS["temperature_c"]["high_red"]:
            flags.append(f"Temperature {temp}°C — CRITICAL")
            level = "RED"
        elif temp >= VITAL_THRESHOLDS["temperature_c"]["high_yellow"]:
            flags.append(f"Temperature {temp}°C — fever")
            if level != "RED": level = "YELLOW"

    spo2 = vitals.get("spo2")
    if spo2 is not None:
        if spo2 < VITAL_THRESHOLDS["spo2"]["critical"]:
            flags.append(f"SpO2 {spo2}% — CRITICAL hypoxia")
            level = "RED"
        elif spo2 < VITAL_THRESHOLDS["spo2"]["warning"]:
            flags.append(f"SpO2 {spo2}% — low oxygen")
            if level != "RED": level = "YELLOW"

    sbp = vitals.get("systolic_bp")
    if sbp is not None:
        if sbp < VITAL_THRESHOLDS["systolic_bp"]["low_red"] or sbp >= VITAL_THRESHOLDS["systolic_bp"]["high_red"]:
            flags.append(f"Systolic BP {sbp} mmHg — CRITICAL")
            level = "RED"
        elif sbp < VITAL_THRESHOLDS["systolic_bp"]["low_yellow"] or sbp >= VITAL_THRESHOLDS["systolic_bp"]["high_yellow"]:
            flags.append(f"Systolic BP {sbp} mmHg — abnormal")
            if level != "RED": level = "YELLOW"

    return {
        "risk_level": level,
        "flags": flags,
        "summary": f"{len(flags)} vital sign alert(s) detected." if flags else "All vitals within acceptable range.",
    }


def get_referral_guidance(urgency_level: str) -> dict:
    """Get referral and transfer guidance based on triage urgency level."""
    urgency_level = urgency_level.upper()
    if urgency_level not in REFERRAL_DATA:
        urgency_level = "YELLOW"
    return REFERRAL_DATA[urgency_level]
