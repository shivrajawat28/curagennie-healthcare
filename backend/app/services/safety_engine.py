"""Safety engine for acute red-flag screening, negation resolution, temporal filtering,
symptom ownership checks, and resolved vs ongoing symptom evaluation.
Executes before any standard consultation follow-up question.
"""

import re
from typing import List, Dict, Optional, Tuple, Any
from app.medical_data.red_flags import (
    RED_FLAG_DEFINITIONS,
    NEGATION_WORDS,
    PAST_TEMPORAL_MARKERS,
    RESOLVED_MARKERS,
    ONGOING_MARKERS,
    OTHER_PERSON_MARKERS,
    AMBIGUITY_MARKERS,
    EMERGENCY_NUMBER,
    AMBULANCE_NUMBER,
)


class SafetyEvaluationResult:
    def __init__(
        self,
        is_emergency: bool,
        is_ambiguous: bool,
        triggered_flags: List[str],
        emergency_title: Optional[str] = None,
        emergency_message: Optional[str] = None,
        clarification_prompt: Optional[str] = None,
        is_historical: bool = False,
        is_other_person: bool = False,
    ):
        self.is_emergency = is_emergency
        self.is_ambiguous = is_ambiguous
        self.triggered_flags = triggered_flags
        self.emergency_title = emergency_title
        self.emergency_message = emergency_message
        self.clarification_prompt = clarification_prompt
        self.is_historical = is_historical
        self.is_other_person = is_other_person

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_emergency": self.is_emergency,
            "is_ambiguous": self.is_ambiguous,
            "triggered_flags": self.triggered_flags,
            "emergency_title": self.emergency_title,
            "emergency_message": self.emergency_message,
            "clarification_prompt": self.clarification_prompt,
            "is_historical": self.is_historical,
            "is_other_person": self.is_other_person,
        }


class SafetyEngine:
    def __init__(self):
        # Precompile regex boundaries with full Unicode awareness (including Devanagari range)
        boundary_prefix = r"(?<![a-zA-Z0-9\u0900-\u097F])("
        boundary_suffix = r")(?![a-zA-Z0-9\u0900-\u097F])"

        self.negation_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in NEGATION_WORDS) + boundary_suffix,
            re.IGNORECASE,
        )
        self.temporal_past_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in PAST_TEMPORAL_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )
        self.resolved_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in RESOLVED_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )
        self.ongoing_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in ONGOING_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )
        self.other_person_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in OTHER_PERSON_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )
        self.ambiguity_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in AMBIGUITY_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )

    def evaluate(self, text: str, language: Optional[str] = None) -> SafetyEvaluationResult:
        """Evaluates raw user input for immediate emergency warning signs."""
        text_clean = text.strip()
        text_lower = text_clean.lower()

        # Auto-detect language if not explicitly provided
        if not language:
            if re.search(r"[\u0900-\u097F]", text_clean):
                lang = "hi"
            elif any(w in text_lower for w in ["hai", "nahi", "mujhe", "mera", "dard", "aur", "par"]):
                lang = "hinglish"
            else:
                lang = "en"
        else:
            lang = language.lower()

        # Split text into grammatical clauses
        clauses = re.split(r"[,;।\.\n]|(\blekin\b|\bparantu\b|\bbut\b|\baur\b|\band\b)", text_clean, flags=re.IGNORECASE)
        clauses = [c.strip() for c in clauses if c and c.strip()]

        triggered_emergencies: List[str] = []
        ambiguous_mentions: List[str] = []
        historical_mentions: List[str] = []
        other_person_mentions: List[str] = []
        resolved_mentions: List[str] = []

        # Detect if multiple subjects are referenced (e.g. self vs family member)
        has_self_reference = bool(re.search(r"\b(i\b|i am|i have|me\b|my\b|mine|mujhe|mera|meri|mere|mai|main)\b", text_lower))
        has_other_reference = bool(self.other_person_re.search(text_lower))
        has_multiple_people = has_self_reference and has_other_reference

        for flag_id, flag_data in RED_FLAG_DEFINITIONS.items():
            keywords = flag_data["keywords"]

            for clause in clauses:
                clause_lower = clause.lower()

                # Check if any keyword in this red-flag appears in the clause
                keyword_match = None
                for kw in keywords:
                    pattern = r"(?<!\w)" + re.escape(kw) + r"(?!\w)"
                    if re.search(pattern, clause_lower):
                        keyword_match = kw
                        break

                if not keyword_match:
                    continue

                # 1. Check for Negation within window around keyword
                # E.g. "I do not have chest pain", "chhati me dard nahi hai"
                if self._is_negated(clause_lower, keyword_match):
                    continue

                # 2. Check for Multiple People / Ambiguous Ownership
                # E.g. "My father had chest pain, but I am feeling headache"
                clause_has_other = bool(self.other_person_re.search(clause_lower))
                if has_multiple_people and clause_has_other:
                    if self._is_historical(clause_lower, text_lower):
                        historical_mentions.append(flag_id)
                    else:
                        other_person_mentions.append(flag_id)
                    continue

                # If another person is mentioned without multiple subjects (e.g. "Mere dost ko chhati me tez dard ho raha hai")
                if clause_has_other:
                    if self._is_historical(clause_lower, text_lower):
                        historical_mentions.append(flag_id)
                        continue
                    # If it's a non-acute ambiguous third party mention:
                    if "dost" in clause_lower or "friend" in clause_lower or "neighbor" in clause_lower or "padosi" in clause_lower or "someone" in clause_lower:
                        other_person_mentions.append(flag_id)
                        continue

                # 3. Check for Resolved vs Ongoing status
                if self._is_resolved(clause_lower, text_lower) and not self._is_ongoing(clause_lower):
                    resolved_mentions.append(flag_id)
                    continue

                # 4. Check for Historical Context (Past)
                # E.g. "I had chest pain last month", "pichle saal behosh hua tha"
                if self._is_historical(clause_lower, text_lower) and not self._is_ongoing(clause_lower):
                    historical_mentions.append(flag_id)
                    continue

                # 5. Check for Uncertainty / Ambiguity
                # E.g. "maybe chest pain or gas", "pata nahi chhati me dabav hai ya nahi"
                if self._is_ambiguous(clause_lower):
                    ambiguous_mentions.append(flag_id)
                    continue

                # Active Current Emergency Detected
                triggered_emergencies.append(flag_id)

        # Priority 1: Definite Active Emergency
        if triggered_emergencies:
            first_flag_id = triggered_emergencies[0]
            flag_info = RED_FLAG_DEFINITIONS[first_flag_id]
            title = flag_info["title"]
            
            if lang in ["hi", "hinglish"]:
                msg = (
                    f"⚠️ आपातकालीन चेतावनी (Emergency Alert): आपके विवरण में गंभीर चेतावनी संकेत मिले हैं ({title})। "
                    f"नियमित पूछताछ रोक दी गई है। कृपया समय न गंवाएं: तत्काल भारत की राष्ट्रीय आपातकालीन सेवा 112 या "
                    f"108 (एम्बुलेंस) पर कॉल करें और निकटतम इमरजेंसी अस्पताल पहुंचें। "
                    f"CuraGennie केवल एक डिजिटल मार्गदर्शक है और स्वयं आपातकालीन सेवाएं या एम्बुलेंस नहीं भेजता है।"
                )
            else:
                msg = (
                    f"⚠️ CRITICAL EMERGENCY WARNING: Your reported symptoms indicate an urgent warning sign ({title}). "
                    f"Routine questioning has been stopped. Please do not delay: immediately call 112 (National Emergency Helpline) "
                    f"or local ambulance services (108 in India), and proceed to the nearest emergency department. "
                    f"CuraGennie provides guidance only and does not dispatch emergency services or ambulances."
                )

            return SafetyEvaluationResult(
                is_emergency=True,
                is_ambiguous=False,
                triggered_flags=triggered_emergencies,
                emergency_title=title,
                emergency_message=msg,
                is_historical=False,
            )

        # Priority 2: Symptom Ownership / Other Person Ambiguity
        if other_person_mentions:
            first_flag_id = other_person_mentions[0]
            title = RED_FLAG_DEFINITIONS[first_flag_id]["title"]

            if lang in ["hi", "hinglish"]:
                clarify_msg = (
                    f"आपने किसी अन्य व्यक्ति के संदर्भ में एक गंभीर चेतावनी संकेत ({title}) का उल्लेख किया है। "
                    f"सुरक्षा के लिए स्पष्ट करें: क्या यह लक्षण आपको हो रहा है या किसी अन्य व्यक्ति को, और क्या वे इस समय गंभीर स्थिति में हैं? "
                    f"यदि कोई भी व्यक्ति इस समय सीने में तेज दर्द, सांस लेने में असमर्थता या बेहोशी की स्थिति में है, तो तुरंत 112 डायल करें।"
                )
            else:
                clarify_msg = (
                    f"You mentioned an urgent health symptom ({title}) in connection with another person. "
                    f"For patient safety, please clarify: Who is experiencing this symptom, and are they currently in distress? "
                    f"If anyone present with you is experiencing severe chest pain, breathing difficulty, or loss of consciousness right now, please call 112 immediately."
                )

            return SafetyEvaluationResult(
                is_emergency=False,
                is_ambiguous=True,
                triggered_flags=other_person_mentions,
                clarification_prompt=clarify_msg,
                is_other_person=True,
            )

        # Priority 3: Resolved Acute Symptom Ambiguity
        if resolved_mentions:
            first_flag_id = resolved_mentions[0]
            title = RED_FLAG_DEFINITIONS[first_flag_id]["title"]

            if lang in ["hi", "hinglish"]:
                clarify_msg = (
                    f"आपने एक गंभीर लक्षण ({title}) का उल्लेख किया है जो अब ठीक या बंद हो चुका है। "
                    f"अस्थायी लक्षण भी चिकित्सकीय दृष्टि से महत्वपूर्ण हो सकते हैं। कृपया स्पष्ट करें: क्या दर्द/तकलीफ पूरी तरह समाप्त हो चुकी है, "
                    f"या अभी भी हल्का दबाव, सांस फूलना या कमजोरी महसूस हो रही है? यदि लक्षण फिर से उभरें, तो तुरंत 112 डायल करें।"
                )
            else:
                clarify_msg = (
                    f"You mentioned an urgent symptom ({title}) that has since stopped or resolved. "
                    f"Even transient warning signs warrant medical caution. Please clarify: Has this symptom completely cleared without any remaining chest pressure, breathlessness, or weakness? If any symptoms return or persist, please seek emergency medical evaluation immediately (Call 112)."
                )

            return SafetyEvaluationResult(
                is_emergency=False,
                is_ambiguous=True,
                triggered_flags=resolved_mentions,
                clarification_prompt=clarify_msg,
            )

        # Priority 4: General Ambiguity
        if ambiguous_mentions:
            first_ambiguous_id = ambiguous_mentions[0]
            title = RED_FLAG_DEFINITIONS[first_ambiguous_id]["title"]

            if lang in ["hi", "hinglish"]:
                clarify_msg = (
                    f"आपने एक महत्वपूर्ण स्वास्थ्य संकेत ({title}) का अस्पष्ट उल्लेख किया है। "
                    f"सुरक्षा के लिए स्पष्ट करें: क्या आपको इस समय सीने में तेज दर्द, सांस लेने में असमर्थता "
                    f"या कोई गंभीर आपातकालीन लक्षण महसूस हो रहा है? (यदि हां, तो तुरंत 112 डायल करें।)"
                )
            else:
                clarify_msg = (
                    f"You mentioned a potentially urgent health concern ({title}) with uncertainty. "
                    f"For your medical safety, please clarify: Are you experiencing severe chest tightness, "
                    f"inability to breathe, or sudden severe symptoms right now? (If yes, please call 112 immediately.)"
                )

            return SafetyEvaluationResult(
                is_emergency=False,
                is_ambiguous=True,
                triggered_flags=ambiguous_mentions,
                clarification_prompt=clarify_msg,
                is_historical=False,
            )

        # Priority 5: Historical Mention Only
        if historical_mentions:
            return SafetyEvaluationResult(
                is_emergency=False,
                is_ambiguous=False,
                triggered_flags=[],
                is_historical=True,
            )

        # Clean / Normal Safety Profile
        return SafetyEvaluationResult(
            is_emergency=False,
            is_ambiguous=False,
            triggered_flags=[],
            is_historical=False,
        )

    def _is_negated(self, clause: str, keyword: str) -> bool:
        """Determines if the keyword in clause is negated using proximity windows."""
        negation_match = self.negation_re.search(clause)
        if not negation_match:
            return False

        # If negation word appears in the clause, inspect word distance
        words = clause.split()
        kw_words = keyword.split()
        
        try:
            kw_first_word = kw_words[0]
            for i, w in enumerate(words):
                clean_w = re.sub(r"[^\w]", "", w)
                if clean_w == kw_first_word:
                    # Look at 4 words before and 4 words after
                    window = words[max(0, i - 4) : min(len(words), i + len(kw_words) + 4)]
                    window_text = " ".join(window)
                    if self.negation_re.search(window_text):
                        return True
        except Exception:
            pass

        return bool(negation_match)

    def _is_other_person(self, clause: str, full_text: str) -> bool:
        """Checks if the clause or enclosing sentence references another person."""
        return bool(self.other_person_re.search(clause) or self.other_person_re.search(full_text))

    def _is_resolved(self, clause: str, full_text: str) -> bool:
        """Checks if a symptom is explicitly described as resolved, gone, or stopped."""
        return bool(self.resolved_re.search(clause) or self.resolved_re.search(full_text))

    def _is_ongoing(self, clause: str) -> bool:
        """Checks if a symptom is explicitly described as continuing or active right now."""
        return bool(self.ongoing_re.search(clause))

    def _is_historical(self, clause: str, full_text: str) -> bool:
        """Checks if the clause or enclosing sentence references past timeframes."""
        return bool(self.temporal_past_re.search(clause) or self.temporal_past_re.search(full_text))

    def _is_ambiguous(self, clause: str) -> bool:
        """Checks if the clause expresses doubt or ambiguity regarding an emergency symptom."""
        return bool(self.ambiguity_re.search(clause))


safety_engine = SafetyEngine()
