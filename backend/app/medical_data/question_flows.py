"""Structured consultation pathways for the 4 core presentations:
Fever, Cough, Headache, and Abdominal Pain.
Maximum 4 targeted clinical follow-up questions per pathway.
"""

from typing import Dict, List, Any

PATHWAY_FEVER = "fever"
PATHWAY_COUGH = "cough"
PATHWAY_HEADACHE = "headache"
PATHWAY_ABDOMINAL_PAIN = "abdominal_pain"
PATHWAY_GENERAL = "general"

QUESTION_FLOWS: Dict[str, List[Dict[str, Any]]] = {
    PATHWAY_FEVER: [
        {
            "id": "fever_duration",
            "key": "duration",
            "question_en": "How many days have you had this fever, and has it been continuous or coming and going?",
            "question_hi": "आपको बुखार कितने दिनों से है, और क्या यह लगातार है या उतर-चढ़ रहा है?",
            "question_hinglish": "Aapko bukhar kitne dino se hai, aur kya ye lagatar bana hua hai ya utar-chadh raha hai?",
            "skip_if_entities": ["fever_duration", "duration"],
            "category": "timeline",
        },
        {
            "id": "fever_temperature",
            "key": "temperature",
            "question_en": "Have you measured your temperature with a thermometer? If so, what was the highest reading?",
            "question_hi": "क्या आपने थर्मामीटर से बुखार नापा है? यदि हां, तो कितना तापमान था?",
            "question_hinglish": "Kya aapne thermometer se bukhar naapa hai? Agar haan, toh kitna reading aaya tha?",
            "skip_if_entities": ["temperature_reading", "measured_temperature"],
            "category": "severity",
        },
        {
            "id": "fever_associated",
            "key": "associated_symptoms",
            "question_en": "Are you experiencing chills/shivering, severe body pain, or any visible skin rashes?",
            "question_hi": "क्या आपको ठंड लगकर कंपकंपी, तेज बदन दर्द या शरीर पर कोई लाल दाने दिख रहे हैं?",
            "question_hinglish": "Kya aapko thand lag kar kapkapi, tez badan dard ya sharir par laal daane (rashes) dikh rahe hain?",
            "skip_if_entities": ["chills", "rash", "body_pain"],
            "category": "differential",
        },
        {
            "id": "fever_hydration_warning",
            "key": "hydration_severity",
            "question_en": "Are you able to drink water and fluids adequately, or are you noticing persistent vomiting or severe dizziness?",
            "question_hi": "क्या आप पर्याप्त पानी और तरल पदार्थ पी पा रहे हैं, या लगातार उल्टी और कमजोरी महसूस हो रही है?",
            "question_hinglish": "Kya aap paani aur fluids theek se pee pa rahe hain, ya lagatar ulti aur chakkar aa rahe hain?",
            "skip_if_entities": ["hydration_status", "intractable_vomiting"],
            "category": "red_flag_screen",
        },
    ],
    PATHWAY_COUGH: [
        {
            "id": "cough_duration",
            "key": "duration",
            "question_en": "How long have you been coughing, and did it start after a cold or throat irritation?",
            "question_hi": "आपको खांसी कितने दिनों से है, और क्या यह सर्दी या गले में खराश के बाद शुरू हुई?",
            "question_hinglish": "Aapko khansi kitne dino se ho rahi hai, aur kya ye sardi ya gale me kharash ke baad shuru hui?",
            "skip_if_entities": ["cough_duration", "duration"],
            "category": "timeline",
        },
        {
            "id": "cough_type",
            "key": "cough_type",
            "question_en": "Is it a dry, scratchy cough, or are you bringing up phlegm/mucus? If mucus, what color is it?",
            "question_hi": "क्या यह सूखी खांसी है, या बलगम आ रहा है? यदि बलगम है तो किस रंग का है?",
            "question_hinglish": "Khansi sookhi (dry) hai ya balgam (phlegm) nikal raha hai? Agar balgam hai toh kaisa rang hai?",
            "skip_if_entities": ["dry_cough", "productive_cough", "phlegm"],
            "category": "characteristics",
        },
        {
            "id": "cough_associated",
            "key": "associated_symptoms",
            "question_en": "Do you also have a fever, runny nose, or pain in your chest when you cough?",
            "question_hi": "क्या साथ में बुखार, बहती नाक या खांसते समय सीने में खिंचाव/दर्द भी महसूस होता है?",
            "question_hinglish": "Kya sath me bukhar, beh rahi naak ya khaste waqt chhati me khinchav/dard hota hai?",
            "skip_if_entities": ["fever", "runny_nose", "chest_discomfort"],
            "category": "differential",
        },
        {
            "id": "cough_breathing_warning",
            "key": "breathing_warning",
            "question_en": "Are you feeling short of breath during routine activities, or wheezing/whistling sounds when you breathe?",
            "question_hi": "क्या सामान्य कामकाज में भी सांस फूल रही है, या सांस लेते समय सीटी जैसी आवाज (wheezing) आ रही है?",
            "question_hinglish": "Kya aam kaam karte waqt bhi saans phool rahi hai, ya saans lete waqt seeti jaisi awaaz aa rahi hai?",
            "skip_if_entities": ["breathing_difficulty", "wheezing"],
            "category": "red_flag_screen",
        },
    ],
    PATHWAY_HEADACHE: [
        {
            "id": "headache_onset_duration",
            "key": "onset_and_duration",
            "question_en": "How long have you had this headache, and did it develop gradually or begin suddenly?",
            "question_hi": "आपको सिर दर्द कितने समय से है, और क्या यह धीरे-धीरे बढ़ा या अचानक शुरू हुआ?",
            "question_hinglish": "Aapko sar dard kitne samay se hai, aur kya ye dheere-dheere badha ya achanak tez shuru hua?",
            "skip_if_entities": ["headache_duration", "onset_type", "duration"],
            "category": "timeline",
        },
        {
            "id": "headache_location_severity",
            "key": "location_and_severity",
            "question_en": "Where is the pain mostly felt (forehead, temples, one side, or back of head), and how severe is it from 1 to 10?",
            "question_hi": "दर्द मुख्य रूप से कहां महसूस हो रहा है (माथे पर, एक तरफ, या सिर के पीछे), और 1 से 10 के पैमाने पर कितना तेज है?",
            "question_hinglish": "Dard sar me kis jagah zyada hai (maathe par, ek taraf, ya peechhe), aur 1 se 10 ke scale par kitna tez hai?",
            "skip_if_entities": ["headache_location", "severity_scale"],
            "category": "characteristics",
        },
        {
            "id": "headache_associated",
            "key": "associated_symptoms",
            "question_en": "Do you also notice nausea, sensitivity to bright lights or loud sounds, or blurred vision?",
            "question_hi": "क्या साथ में जी मिचलाना, तेज रोशनी/आवाज से परेशानी, या आंखों के आगे धुंधलापन आ रहा है?",
            "question_hinglish": "Kya sath me ulti jaisa lagna, tez roshni ya awaaz se pareshani, ya dhundhla dikhai de raha hai?",
            "skip_if_entities": ["photophobia", "nausea_vomiting", "vision_blur"],
            "category": "differential",
        },
        {
            "id": "headache_neurological_warning",
            "key": "neurological_warning",
            "question_en": "Do you have any neck stiffness when bending your chin to your chest, high fever, or weakness in your arms or legs?",
            "question_hi": "क्या गर्दन में अकड़न, तेज बुखार, या हाथ-पैरों में किसी तरह की कमजोरी महसूस हो रही है?",
            "question_hinglish": "Kya gardan me jakdan/akad, tez bukhar, ya haath-pair me koi kamzori mehsoos ho rahi hai?",
            "skip_if_entities": ["neck_stiffness", "focal_weakness"],
            "category": "red_flag_screen",
        },
    ],
    PATHWAY_ABDOMINAL_PAIN: [
        {
            "id": "abd_location_duration",
            "key": "location_and_duration",
            "question_en": "Where exactly in your abdomen is the pain (upper stomach, lower right/left, or generalized), and how long has it lasted?",
            "question_hi": "पेट में दर्द किस जगह पर है (ऊपरी पेट, नाभि के पास, नीचे दाईं/बाईं तरफ), और यह कितनी देर से है?",
            "question_hinglish": "Pet me dard kis jagah ho raha hai (upar pet me, naabhi ke aas-paas, ya neeche), aur kitni der se hai?",
            "skip_if_entities": ["abdominal_location", "abdominal_duration", "duration"],
            "category": "timeline",
        },
        {
            "id": "abd_nature_pain",
            "key": "pain_nature",
            "question_en": "Is the pain a burning feeling, dull ache, or sharp cramping that comes and goes in waves?",
            "question_hi": "क्या दर्द में जलन है, हल्का भारीपन है, या रुक-रुक कर तेज मरोड़ (cramps) उठ रहे हैं?",
            "question_hinglish": "Kya dard me jalan (acidity) hai, bhari sa dard hai, ya ruk-ruk kar tez marod (cramps) uth rahe hain?",
            "skip_if_entities": ["pain_type", "burning_acidity", "cramping"],
            "category": "characteristics",
        },
        {
            "id": "abd_digestive_associated",
            "key": "digestive_symptoms",
            "question_en": "Have you had any vomiting, loose stools (diarrhea), or difficulty passing gas or bowel movements?",
            "question_hi": "क्या आपको उल्टी, पतले दस्त (लूज मोशन), या पेट साफ न होने की समस्या हो रही है?",
            "question_hinglish": "Kya ulti, loose motions, ya pet theek se saaf na hone ki pareshani ho rahi hai?",
            "skip_if_entities": ["nausea_vomiting", "diarrhea", "constipation"],
            "category": "differential",
        },
        {
            "id": "abd_warning_signs",
            "key": "acute_warning",
            "question_en": "Is your belly noticeably rigid or excruciating to light touch, or have you noticed blood in vomit or stools?",
            "question_hi": "क्या पेट छूने पर पत्थर जैसा सख्त व अत्यधिक दर्दनाक है, या उल्टी अथवा शौच में खून दिखा है?",
            "question_hinglish": "Kya pet chhoone par behad sakht ya asahniya dard ho raha hai, ya ulti ya potty me khoon dikha hai?",
            "skip_if_entities": ["rigid_abdomen", "gastrointestinal_bleeding"],
            "category": "red_flag_screen",
        },
    ],
    PATHWAY_GENERAL: [
        {
            "id": "gen_duration",
            "key": "duration",
            "question_en": "How many days have you been feeling this way, and are the symptoms getting better, worse, or staying the same?",
            "question_hi": "आप कितने दिनों से ऐसा महसूस कर रहे हैं, और क्या लक्षण बढ़ रहे हैं या वैसे ही बने हुए हैं?",
            "question_hinglish": "Aapko ye pareshani kitne dino se ho rahi hai, aur kya lakshan badh rahe hain ya waise hi hain?",
            "skip_if_entities": ["duration"],
            "category": "timeline",
        },
        {
            "id": "gen_severity",
            "key": "severity",
            "question_en": "How severely is this impacting your daily routine, sleep, or ability to eat and drink?",
            "question_hi": "इस समस्या से आपकी दिनचर्या, नींद, या खान-पान पर कितना असर पड़ रहा है?",
            "question_hinglish": "Is pareshani se aapke rozana ke kaam, neend, ya khane-peene par kitna asar pad raha hai?",
            "skip_if_entities": ["severity"],
            "category": "severity",
        },
        {
            "id": "gen_other_symptoms",
            "key": "associated",
            "question_en": "Are there any other symptoms you are noticing, such as fever, cough, nausea, or body aches?",
            "question_hi": "क्या आपको बुखार, खांसी, उल्टी या बदन दर्द जैसा कोई अन्य लक्षण भी महसूस हो रहा है?",
            "question_hinglish": "Kya aapko bukhar, khansi, ulti ya badan dard jaisa koi aur lakshan bhi mehsoos ho raha hai?",
            "skip_if_entities": ["other_symptoms"],
            "category": "differential",
        },
    ],
}
