"""
Medical protocol seed data for the local ChromaDB vector store.
Sources: WHO Emergency Triage (ETAT+), MSF Clinical Guidelines (public domain).
"""

PROTOCOLS = [
    {
        "id": "wound-001",
        "title": "Wound Assessment & Triage",
        "content": (
            "ASSESS: Size, depth, contamination, signs of infection (redness, warmth, swelling, pus). "
            "RED FLAGS: Wound >5cm deep, bone/tendon visible, heavy contamination, signs of sepsis (fever >38.5°C, confusion, rapid breathing). "
            "ACTION: Clean with clean water + soap. Cover with clean dressing. "
            "REFER URGENTLY if: red flags present, wound >8h old and contaminated, patient immunocompromised or diabetic. "
            "TETANUS: Give booster if last dose >5y ago or unknown."
        ),
        "category": "trauma",
    },
    {
        "id": "burn-001",
        "title": "Burn Assessment & First Aid",
        "content": (
            "CLASSIFY: Superficial (red, painful, no blisters), Partial thickness (blisters, very painful), Full thickness (white/charred, painless). "
            "BODY SURFACE AREA (BSA): Palm = 1%. "
            "RED FLAGS: >10% BSA any burn, >5% partial/full thickness, burns to face/hands/genitals/joints, circumferential burns, inhalation injury (singed nose hair, hoarse voice, soot in mouth). "
            "ACTION: Cool with running water 20min (NOT ice). Remove jewelry. Do NOT burst blisters. Cover with clean non-fluffy dressing. "
            "REFER URGENTLY if: any red flag present, child <5y or adult >60y with significant burn."
        ),
        "category": "trauma",
    },
    {
        "id": "fever-001",
        "title": "Fever Triage in Resource-Limited Settings",
        "content": (
            "MEASURE: Temperature. >38°C = fever. >40°C = high risk. "
            "ASSESS FOR MALARIA: In endemic area — fever + chills + sweating. Perform RDT if available. "
            "ASSESS FOR SEPSIS: Fever + confusion/lethargy + fast breathing + low BP = EMERGENCY. "
            "ASSESS FOR MENINGITIS: Fever + stiff neck + photophobia + rash = EMERGENCY. "
            "RED FLAGS (refer immediately): altered consciousness, seizures, unable to drink, severe vomiting, fast/difficult breathing, cold extremities. "
            "ACTION: Paracetamol for fever. Oral rehydration if tolerated. Treat malaria per national protocol if RDT positive."
        ),
        "category": "infectious",
    },
    {
        "id": "resp-001",
        "title": "Respiratory Distress Assessment",
        "content": (
            "SIGNS: Count breaths per minute. Adult >30/min = danger. Child >50/min (infant) or >40/min (1-5y) = danger. "
            "ASSESS: Oxygen saturation if pulse ox available (<90% = danger). Cyanosis. Use of accessory muscles. Inability to speak full sentences. "
            "CAUSES TO CONSIDER: Pneumonia (fever + productive cough + crackles), Asthma (wheeze, history), Heart failure (bilateral crackles, leg swelling), TB (chronic cough >2wk + weight loss + night sweats). "
            "RED FLAGS: SpO2 <90%, cyanosis, silent chest, exhausted patient unable to maintain breathing effort. "
            "ACTION: Sit patient upright. Give oxygen if available. REFER URGENTLY for all red flags."
        ),
        "category": "respiratory",
    },
    {
        "id": "skin-001",
        "title": "Skin Lesion & Rash Assessment",
        "content": (
            "DESCRIBE: Distribution (localized vs widespread), morphology (macule/papule/vesicle/pustule/ulcer), color, border. "
            "RED FLAGS: Petechiae/purpura (non-blanching rash) + fever = possible meningococcemia — EMERGENCY. Widespread blistering/skin peeling (Stevens-Johnson). Rapidly spreading redness + warmth + systemic illness (necrotizing fasciitis). "
            "COMMON CONDITIONS: Scabies (itchy burrows between fingers), Tinea (scaling ring lesion), Impetigo (honey-crusted lesions), Cellulitis (red/warm/swollen skin, usually one limb). "
            "ACTION FOR CELLULITIS: Antibiotics (amoxicillin-clavulanate if available). Elevate limb. REFER if spreading rapidly or systemic signs."
        ),
        "category": "dermatology",
    },
    {
        "id": "dehydration-001",
        "title": "Dehydration Assessment & ORT",
        "content": (
            "ASSESS: Skin turgor (pinch abdomen — slow return = dehydrated), sunken eyes, dry mouth, last urination time. "
            "CLASSIFY: Mild (<5% body weight) — thirsty, normal exam. Moderate (5-10%) — sunken eyes, reduced skin turgor, fast pulse. Severe (>10%) — above + lethargic, very sunken eyes, weak/absent pulse. "
            "RED FLAGS: Severe dehydration, unable to drink, blood in stool, cholera suspicion. "
            "ACTION MILD/MODERATE: Oral Rehydration Salts (ORS). 75ml/kg over 4h for moderate. Reassess. "
            "ACTION SEVERE: IV/NG fluids. REFER URGENTLY. Continue ORS during transfer if able to drink."
        ),
        "category": "pediatric",
    },
    {
        "id": "obstetric-001",
        "title": "Obstetric Emergency Red Flags",
        "content": (
            "REFER IMMEDIATELY for any of: heavy vaginal bleeding (>1 pad/15min), severe headache + visual disturbance + high BP in pregnancy (pre-eclampsia), seizure in pregnancy (eclampsia), severe abdominal pain in pregnancy, cord prolapse, prolonged labor >12h, baby not delivered within 1h of pushing. "
            "ECLAMPSIA ACTION: Left lateral position. Airway. Give magnesium sulfate if available (loading dose 4g IV slow). REFER URGENTLY. "
            "PPH ACTION: Uterine massage. Oxytocin 10IU IM if available. IV access. REFER URGENTLY."
        ),
        "category": "obstetric",
    },
    {
        "id": "trauma-head-001",
        "title": "Head Injury Assessment",
        "content": (
            "ASSESS: Glasgow Coma Scale (Eye 1-4, Verbal 1-5, Motor 1-6). GCS <13 = serious. "
            "RED FLAGS: GCS <15 or deteriorating, loss of consciousness >1min, repeated vomiting, severe headache, seizure, clear fluid from nose/ears, unequal pupils, focal neurological signs. "
            "ACTION: Immobilize cervical spine if mechanism warrants (fall from height, RTA). Do NOT give aspirin/NSAIDs. "
            "REFER URGENTLY if any red flag. Observe all head injuries for minimum 4h even if initially well."
        ),
        "category": "trauma",
    },
]
