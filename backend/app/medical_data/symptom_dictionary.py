"""Standardized medical symptom taxonomy and multilingual expression dictionary.
Supports English, Devanagari Hindi, and Romanized Hinglish.
"""

from typing import Dict, List, Set

# Canonical symptom identifiers
FEVER = "fever"
BODY_PAIN = "body_pain"
HEADACHE = "headache"
COUGH = "cough"
NAUSEA_VOMITING = "nausea_vomiting"
ABDOMINAL_PAIN = "abdominal_pain"
BREATHING_DIFFICULTY = "breathing_difficulty"
CHEST_PAIN = "chest_pain"
SORE_THROAT = "sore_throat"
WEAKNESS = "weakness"
RUNNY_NOSE = "runny_nose"
DIARRHEA = "diarrhea"
CHILLS = "chills"
RASH = "rash"
DIZZINESS = "dizziness"

SYMPTOM_METADATA: Dict[str, Dict[str, str]] = {
    FEVER: {"label": "Fever / Elevated Temperature", "category": "systemic"},
    BODY_PAIN: {"label": "Generalized Body Ache / Myalgia", "category": "systemic"},
    HEADACHE: {"label": "Headache / Cephalea", "category": "neurological"},
    COUGH: {"label": "Cough / Respiratory Irritation", "category": "respiratory"},
    NAUSEA_VOMITING: {"label": "Nausea / Emesis", "category": "gastrointestinal"},
    ABDOMINAL_PAIN: {"label": "Abdominal Discomfort / Pain", "category": "gastrointestinal"},
    BREATHING_DIFFICULTY: {"label": "Shortness of Breath / Dyspnea", "category": "cardiorespiratory"},
    CHEST_PAIN: {"label": "Chest Discomfort / Pain", "category": "cardiorespiratory"},
    SORE_THROAT: {"label": "Pharyngitis / Sore Throat", "category": "respiratory"},
    WEAKNESS: {"label": "Lethargy / Asthenia", "category": "systemic"},
    RUNNY_NOSE: {"label": "Rhinorrhea / Congestion", "category": "respiratory"},
    DIARRHEA: {"label": "Loose Stools / Diarrhea", "category": "gastrointestinal"},
    CHILLS: {"label": "Rigors / Chills", "category": "systemic"},
    RASH: {"label": "Skin Eruption / Rash", "category": "dermatological"},
    DIZZINESS: {"label": "Lightheadedness / Vertigo", "category": "neurological"},
}

# Multilingual expression mappings: Phrase -> Canonical Symptom
# Format includes exact phrases and key stems in English, Hinglish, and Hindi
SYMPTOM_EXPRESSIONS: Dict[str, List[str]] = {
    FEVER: [
        # English
        "fever", "high temperature", "running temperature", "feverish", "pyrexia", "hot body",
        "burning up", "mild fever", "high fever", "low grade fever",
        # Hinglish
        "bukhar", "bukhaar", "tez bukhar", "halka bukhar", "taap", "fever hai", "bukhar lag raha",
        "sharir garam", "garam sharir", "tap raha", "bukhar charha",
        # Hindi Devanagari
        "बुखार", "तेज बुखार", "ताप", "ज्वर", "हल्का बुखार", "शरीर गरम",
    ],
    BODY_PAIN: [
        # English
        "body pain", "body ache", "body aches", "muscle pain", "joint pain", "myalgia", "generalized ache",
        # Hinglish
        "body dard", "badan dard", "body mein dard", "badan me dard", "badan toot raha",
        "ang ang dard", "haddi me dard", "sharir dard", "jism me dard", "tootan",
        # Hindi Devanagari
        "बदन दर्द", "शरीर में दर्द", "बदन में दर्द", "अंग अंग दर्द", "हड्डियों में दर्द",
    ],
    HEADACHE: [
        # English
        "headache", "head pain", "migraine", "severe headache", "throbbing head", "temple pain",
        # Hinglish
        "sar dard", "sar me dard", "sar mein dard", "sir dard", "sir me dard", "matha dard",
        "sar fat raha", "sar ghoom raha", "sir me jalan", "adha sar dard",
        # Hindi Devanagari
        "सिर दर्द", "सर दर्द", "सिर में दर्द", "सर में दर्द", "माथा दर्द", "आधा सिर दर्द",
    ],
    COUGH: [
        # English
        "cough", "coughing", "dry cough", "wet cough", "productive cough", "hacking cough", "phlegm", "mucus",
        # Hinglish
        "khansi", "khasi", "khaasi", "sookhi khansi", "sukhi khansi", "balgam wali khansi",
        "balgam", "dhasak", "khansi aa rahi", "cough ho raha",
        # Hindi Devanagari
        "खांसी", "सुखी खांसी", "बलगम वाली खांसी", "कफ", "खंसी",
    ],
    NAUSEA_VOMITING: [
        # English
        "nausea", "vomiting", "vomit", "throwing up", "feeling sick", "queasy", "emesis",
        # Hinglish
        "ulti", "ulti aa rahi", "ulti jaisa", "matli", "ji ghabrana", "ji michlana",
        "qai", "vomit ho rahi", "kai", "vomiting feel ho rahi",
        # Hindi Devanagari
        "उल्टी", "मतली", "जी घबराना", "जी मिचलाना", "वमन",
    ],
    ABDOMINAL_PAIN: [
        # English
        "abdominal pain", "stomach pain", "stomach ache", "belly ache", "tummy ache", "cramps",
        "gastric pain", "gut pain", "pain in stomach", "pain in belly", "pain in abdomen",
        # Hinglish
        "pet dard", "pet me dard", "pet mein dard", "pet me marod", "pet me aintham",
        "pet me jalan", "pet kharab", "stomach me dard", "pet dukh raha",
        "pet me bohot dard", "pet me bahut dard", "pet me tez dard", "pet me bahut tez dard",
        # Hindi Devanagari
        "पेट दर्द", "पेट में दर्द", "पेट में मरोड़", "पेट में ऐंठन", "पेट में जलन",
        "पेट में बहुत तेज दर्द", "पेट में तेज दर्द", "पेट में बहुत दर्द",
    ],
    BREATHING_DIFFICULTY: [
        # English
        "shortness of breath", "difficulty breathing", "breathless", "hard to breathe",
        "gasping", "dyspnea", "struggling to breathe", "winded",
        # Hinglish
        "saans lene me dikkat", "saans phoolna", "saans lene me takleef", "saans ruk rahi",
        "dum ghutna", "saans chadna", "saans nahi aa rahi",
        # Hindi Devanagari
        "सांस लेने में दिक्कत", "सांस फूलना", "सांस की तकलीफ", "दम घुटना",
    ],
    CHEST_PAIN: [
        # English
        "chest pain", "chest pressure", "chest tightness", "pain in chest", "chest discomfort",
        "heaviness in chest", "squeezing in chest",
        # Hinglish
        "chhati me dard", "chhati mein dard", "seene me dard", "seene mein dard",
        "chhati me dabav", "seene me jalan", "chhati bhari",
        # Hindi Devanagari
        "छाती में दर्द", "सीने में दर्द", "छाती में दबाव", "सीने में भारीपन",
    ],
    SORE_THROAT: [
        # English
        "sore throat", "throat pain", "throat irritation", "pain swallowing", "scratchy throat",
        # Hinglish
        "gale me kharash", "gale me dard", "gala baith gaya", "gala kharab", "nigalne me dard",
        # Hindi Devanagari
        "गले में खराश", "गले में दर्द", "गला खराब",
    ],
    WEAKNESS: [
        # English
        "weakness", "extreme fatigue", "exhaustion", "lethargy", "tiredness", "drained",
        # Hinglish
        "kamzori", "thakan", "thakaavat", "sust lag raha", "chakkar aur kamzori", "jaan nahi hai",
        # Hindi Devanagari
        "कमजोरी", "थकान", "सुस्ती",
    ],
    RUNNY_NOSE: [
        # English
        "runny nose", "blocked nose", "nasal congestion", "sneezing", "cold", "stuffy nose",
        # Hinglish
        "naak beh rahi", "zukam", "zukaam", "nazla", "chheenk", "naak band",
        # Hindi Devanagari
        "जुकाम", "सर्दी", "छींक", "नाक बहना",
    ],
    DIARRHEA: [
        # English
        "diarrhea", "loose motion", "watery stools", "frequent motions",
        # Hinglish
        "loose motion", "dast", "pet kharab", "loose motions lag gaye", "patla dast",
        # Hindi Devanagari
        "दस्त", "पतले दस्त", "लूज मोशन",
    ],
    CHILLS: [
        # English
        "chills", "shivering", "feeling cold", "rigors", "trembling with cold",
        # Hinglish
        "thand lagna", "thand lag rahi", "kaanpna", "kapkapi", "sheet",
        # Hindi Devanagari
        "ठंड लगना", "कंपकंपी", "जाड़ा लगना",
    ],
    RASH: [
        # English
        "rash", "skin eruption", "red spots", "hives", "itching rash",
        # Hinglish
        "daane", "laal daane", "rash nikal aya", "khujli wale daane", "sharir par daane",
        # Hindi Devanagari
        "दाने", "लाल दाने", "चकत्ते", "खुजली",
    ],
    DIZZINESS: [
        # English
        "dizziness", "lightheadedness", "fainting feeling", "vertigo", "spinning head",
        # Hinglish
        "chakkar", "chakkar aa rahe", "sir ghoom raha", "sar ghoomna",
        # Hindi Devanagari
        "चक्कर", "चक्कर आना", "सिर घूमना",
    ],
}
