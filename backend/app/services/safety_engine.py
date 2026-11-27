"""Safety engine for acute red-flag screening, negation resolution, and temporal filtering.
Executes before any standard consultation follow-up question.
"""

import re
from typing import List, Dict, Optional, Tuple, Any
from app.medical_data.red_flags import (
    RED_FLAG_DEFINITIONS,
    NEGATION_WORDS,
    PAST_TEMPORAL_MARKERS,
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
    ):
        self.is_emergency = is_emergency
        self.is_ambiguous = is_ambiguous
        self.triggered_flags = triggered_flags
        self.emergency_title = emergency_title
        self.emergency_message = emergency_message
        self.clarification_prompt = clarification_prompt
        self.is_historical = is_historical

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_emergency": self.is_emergency,
            "is_ambiguous": self.is_ambiguous,
            "triggered_flags": self.triggered_flags,
            "emergency_title": self.emergency_title,
            "emergency_message": self.emergency_message,
            "clarification_prompt": self.clarification_prompt,
            "is_historical": self.is_historical,
        }


class SafetyEngine:
    def __init__(self):
        # Precompile regex boundaries for negation, temporal, and ambiguity words with full Unicode awareness
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
        self.ambiguity_re = re.compile(
            boundary_prefix + "|".join(re.escape(w) for w in AMBIGUITY_MARKERS) + boundary_suffix,
            re.IGNORECASE,
        )

    def evaluate(self, text: str, language: str = "hinglish") -> SafetyEvaluationResult:
        """Evaluates raw user input for immediate emergency warning signs."""
        text_clean = text.strip()
        text_lower = text_clean.lower()

        # Split text into grammatical clauses
        clauses = re.split(r"[,;।\.\n]|(\blekin\b|\bparantu\b|\bbut\b|\baur\b|\band\b)", text_clean, flags=re.IGNORECASE)
        clauses = [c.strip() for c in clauses if c and c.strip()]

        triggered_emergencies: List[str] = []
        ambiguous_mentions: List[str] = []
        historical_mentions: List[str] = []

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

                # Rule A: Check for Negation within window around keyword
                # E.g. "I do not have chest pain", "chhati me dard nahi hai"
                if self._is_negated(clause_lower, keyword_match):
                    continue

                # Rule B: Check for Historical Context
                # E.g. "I had chest pain last month", "pichle saal behosh hua tha"
                if self._is_historical(clause_lower, text_lower):
                    historical_mentions.append(flag_id)
                    continue

                # Rule C: Check for Ambiguity
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
            
            if language in ["hi", "hinglish"]:
                msg = (
                    f"⚠️ आपातकालीन चेतावनी (Emergency Alert): आपके विवरण में गंभीर चेतावनी संकेत मिले हैं ({title})। "
                    f"कृपया समय न गंवाएं। तत्काल भारत की राष्ट्रीय आपातकालीन सेवा 112 या 108 (एम्बुलेंस) पर कॉल करें "
                    f"और निकटतम इमरजेंसी अस्पताल पहुंचें। CuraGennie स्वचालित रूप से एम्बुलेंस नहीं भेजता है。"
                )
            else:
                msg = (
                    f"⚠️ CRITICAL EMERGENCY WARNING: Your symptoms indicate an urgent warning sign ({title}). "
                    f"Please do not delay. Call 112 or local emergency ambulance (108 in India) immediately "
                    f"and proceed to the nearest emergency department. CuraGennie does not dispatch ambulances."
                )

            return SafetyEvaluationResult(
                is_emergency=True,
                is_ambiguous=False,
                triggered_flags=triggered_emergencies,
                emergency_title=title,
                emergency_message=msg,
                is_historical=False,
            )

        # Priority 2: Ambiguous Emergency-Related Expression
        if ambiguous_mentions:
            first_ambiguous_id = ambiguous_mentions[0]
            title = RED_FLAG_DEFINITIONS[first_ambiguous_id]["title"]

            if language in ["hi", "hinglish"]:
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

        # Priority 3: Historical Mention Only
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
            # Find start index of keyword
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

        # Fallback: clause-level negation present
        return bool(negation_match)

    def _is_historical(self, clause: str, full_text: str) -> bool:
        """Checks if the clause or enclosing sentence references past timeframes."""
        return bool(self.temporal_past_re.search(clause) or self.temporal_past_re.search(full_text))

    def _is_ambiguous(self, clause: str) -> bool:
        """Checks if the clause expresses doubt or ambiguity regarding an emergency symptom."""
        return bool(self.ambiguity_re.search(clause))


safety_engine = SafetyEngine()
