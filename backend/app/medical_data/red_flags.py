"""Emergency red-flag symptom dictionary, negation patterns, and temporal filters.
Strictly conservative medical safety criteria triggering immediate escalation.
"""

from typing import List, Dict, Any

# Primary Emergency Protocols in India
EMERGENCY_NUMBER = "112"
AMBULANCE_NUMBER = "108"

# Red Flag Categories
RED_FLAG_CHEST_CARDIAC = "chest_cardiac_emergency"
RED_FLAG_RESPIRATORY_DISTRESS = "severe_respiratory_distress"
RED_FLAG_STROKE_FAST = "neurological_stroke_signs"
RED_FLAG_LOSS_OF_CONSCIOUSNESS = "syncope_unconsciousness"
RED_FLAG_SEVERE_HEMORRHAGE = "severe_bleeding"
RED_FLAG_ANAPHYLAXIS = "severe_allergic_reaction"
RED_FLAG_THUNDERCLAP_HEADACHE = "thunderclap_acute_headache"
RED_FLAG_ACUTE_ABDOMEN = "acute_rigid_abdomen"

RED_FLAG_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    RED_FLAG_CHEST_CARDIAC: {
        "title": "Suspected Acute Cardiac or Severe Chest Condition",
        "description": "Severe, crushing, or squeezing chest pain, especially radiating to the left arm, neck, or jaw, or accompanied by cold sweats.",
        "emergency_advice": "Stop all exertion immediately. Do not drive yourself. Call 112 or local ambulance immediately for emergency medical transport.",
        "keywords": [
            # English
            "severe chest pain", "crushing chest pain", "chest pain radiating", "radiating to arm",
            "radiating to left arm", "radiating to jaw", "chest pain with sweat", "chest pressure and sweating",
            "heart attack feeling", "crushing pressure on chest", "chest pain", "chest pressure",
            # Hinglish
            "chhati me tez dard", "seene me bahut tez dard", "dard baye haath me ja raha",
            "chhati me dabav aur pasina", "seene me jalan aur pasina", "chhati me asahniya dard",
            "chhati me dard", "seene me dard", "chhati me dabav",
            # Hindi
            "छाती में असहनीय दर्द", "सीने में तेज दर्द", "दर्द बाएं हाथ में", "छाती में तेज दबाव",
            "छाती में दर्द", "सीने में दर्द",
        ],
    },
    RED_FLAG_RESPIRATORY_DISTRESS: {
        "title": "Severe Respiratory Distress",
        "description": "Inability to breathe adequately, gasping for air, blue-colored lips/face, or inability to speak full sentences.",
        "emergency_advice": "Sit upright in a well-ventilated space. Seek immediate emergency care at the nearest hospital or call 112 / 108.",
        "keywords": [
            # English
            "cannot breathe", "unable to breathe", "gasping for air", "lips turning blue",
            "choking", "severe shortness of breath", "struggling for every breath",
            # Hinglish
            "saans bilkul nahi le pa raha", "saans atak rahi hai", "dum ghut raha hai",
            "neele pad gaye lips", "saans lene me behad takleef",
            # Hindi
            "सांस बिल्कुल नहीं आ रही", "दम घुट रहा है", "सांस रुक रही है",
        ],
    },
    RED_FLAG_STROKE_FAST: {
        "title": "Suspected Stroke (FAST Signs)",
        "description": "Sudden facial asymmetry/droop, arm weakness/numbness, or sudden slurring/loss of speech.",
        "emergency_advice": "Time is critical. Note the time symptoms started and reach a stroke-ready emergency hospital immediately via 112 / 108.",
        "keywords": [
            # English
            "facial drooping", "face droop", "slurred speech", "unable to speak",
            "arm weakness on one side", "one side of body paralyzed", "sudden numbness one side",
            # Hinglish
            "chehra tedha ho gaya", "bol nahi pa raha", "awaz ladkhada rahi hai",
            "ek taraf ka haath kaam nahi kar raha", "ek taraf sunn pad gaya",
            # Hindi
            "चेहरा टेढ़ा हो गया", "आवाज लड़खड़ा रही है", "एक तरफ का हाथ काम नहीं कर रहा",
        ],
    },
    RED_FLAG_LOSS_OF_CONSCIOUSNESS: {
        "title": "Loss of Consciousness or Sudden Unresponsiveness",
        "description": "Fainting, syncope, passing out, or inability to remain conscious.",
        "emergency_advice": "Place person on their side in recovery position if breathing. Do not give liquids. Call 112 immediately.",
        "keywords": [
            # English
            "passed out", "loss of consciousness", "fainted suddenly", "unconscious", "blacked out", "fainted",
            # Hinglish
            "behosh ho gaya", "behosh ho gayi", "chakkar aake gir gaya", "sudh budh kho gaya", "behosh hua", "behosh",
            # Hindi
            "बेहोश हो गया", "बेहोश हो गई", "अचेत", "बेहोश",
        ],
    },
    RED_FLAG_SEVERE_HEMORRHAGE: {
        "title": "Severe Hemorrhage or Hemoptysis",
        "description": "Coughing up fresh blood, vomiting large amounts of blood, or heavy uncontrolled bleeding.",
        "emergency_advice": "Apply direct pressure to external wounds. Seek immediate trauma/emergency care or call 112.",
        "keywords": [
            # English
            "coughing up blood", "vomiting blood", "coughing blood", "heavy bleeding", "uncontrolled bleeding",
            # Hinglish
            "khoon ki ulti", "khansi me khoon", "khoon nikal raha behad", "balgam me taza khoon",
            # Hindi
            "खून की उल्टी", "खांसी में खून", "खून बह रहा है",
        ],
    },
    RED_FLAG_ANAPHYLAXIS: {
        "title": "Severe Allergic Reaction / Anaphylaxis",
        "description": "Rapid swelling of lips, tongue, or throat causing airway restriction, usually after food, insect sting, or medication.",
        "emergency_advice": "If an epinephrine auto-injector is prescribed, use it immediately as directed. Call 112 without delay.",
        "keywords": [
            # English
            "lips swelling rapidly", "tongue swollen", "throat closing up", "severe allergic reaction", "anaphylaxis",
            # Hinglish
            "hoth soojh gaye", "jeebh soojh gayi", "gala band ho raha hai", "allergy se saans band",
            # Hindi
            "होंठ सूज गए", "जीभ सूज गई", "गला बंद हो रहा है",
        ],
    },
    RED_FLAG_THUNDERCLAP_HEADACHE: {
        "title": "Sudden Severe 'Thunderclap' Headache",
        "description": "Worst headache of your life that reached peak intensity within seconds or minutes, or headache with sudden stiff neck and fever.",
        "emergency_advice": "Requires immediate emergency neurovascular evaluation. Proceed to an emergency department or call 112.",
        "keywords": [
            # English
            "worst headache of my life", "sudden explosive headache", "thunderclap headache", "headache with stiff neck and high fever",
            # Hinglish
            "zindagi ka sabse tez sar dard", "achanak sar fatne jaisa dard", "bijli jaisa sar dard",
            # Hindi
            "जीवन का सबसे तेज सिर दर्द", "अचानक भयंकर सिर दर्द",
        ],
    },
    RED_FLAG_ACUTE_ABDOMEN: {
        "title": "Severe Acute Abdomen",
        "description": "Sudden, excruciating, unbearable abdominal pain, or a rigid board-like stomach accompanied by high fever or repeated vomiting.",
        "emergency_advice": "Do not eat or drink anything. Do not take painkillers before doctor evaluation. Proceed to an emergency surgical facility or call 112.",
        "keywords": [
            # English
            "unbearable stomach pain", "excruciating abdominal pain", "stomach rock hard", "rigid abdomen",
            # Hinglish
            "pet me asahniya dard", "pet pathar jaisa sakht", "dard se tadap raha pet me",
            # Hindi
            "पेट में असहनीय दर्द", "पेट पत्थर जैसा सख्त",
        ],
    },
}

# Negation words: If an expression is immediately preceded or followed by these within a window of words,
# it is treated as a negative mention (e.g. "I do not have chest pain", "chhati me dard nahi hai").
NEGATION_WORDS: List[str] = [
    # English
    "no", "not", "without", "never", "dont", "don't", "denies", "denied",
    "havent", "haven't", "negative", "free of", "neither", "nor", "rule out",
    # Hinglish
    "nahi", "nahin", "nhi", "na", "mat", "bina", "koi nahi", "bilkul nahi",
    # Hindi Devanagari
    "नहीं", "ना", "बिना", "कोई नहीं", "बिल्कुल नहीं",
]

# Temporal indicators signifying past/resolved conditions rather than active emergencies
PAST_TEMPORAL_MARKERS: List[str] = [
    # English
    "last month", "last year", "years ago", "in the past", "history of", "previously",
    "few weeks ago", "months ago", "had previously", "resolved", "recovered from",
    "was having", "used to have", "long ago",
    # Hinglish
    "pichle mahine", "pichle saal", "pehle tha", "pehle hua tha", "theek ho gaya",
    "purana tha", "bahut pehle", "kuch mahine pehle", "purani baat hai",
    # Hindi Devanagari
    "पिछले महीने", "पिछले साल", "पहले था", "पुराना", "पहले हुआ था",
]

# Ambiguity markers: When red flag keywords appear alongside hesitation, prompt for clarification
AMBIGUITY_MARKERS: List[str] = [
    "maybe", "might be", "not sure if", "pata nahi", "shayad", "doubtful",
    "kuch keh nahi sakte", "lagta hai ya nahi", "confusion hai", "perhaps",
    "शायद", "पता नहीं",
]
