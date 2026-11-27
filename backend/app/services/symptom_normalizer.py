"""Multilingual symptom normalizer for English, Hindi, and Hinglish.
Extracts canonical symptoms, negated symptoms, timelines, and severity cues.
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from app.medical_data.symptom_dictionary import (
    SYMPTOM_EXPRESSIONS,
    SYMPTOM_METADATA,
    FEVER,
    COUGH,
    HEADACHE,
    ABDOMINAL_PAIN,
)
from app.medical_data.red_flags import NEGATION_WORDS, PAST_TEMPORAL_MARKERS


class NormalizedExtraction:
    def __init__(
        self,
        original_text: str,
        detected_symptoms: List[str],
        negated_symptoms: List[str],
        timeline: Optional[str] = None,
        severity_cue: Optional[str] = None,
        temperature_reading: Optional[str] = None,
        needs_clarification: bool = False,
    ):
        self.original_text = original_text
        self.detected_symptoms = detected_symptoms
        self.negated_symptoms = negated_symptoms
        self.timeline = timeline
        self.severity_cue = severity_cue
        self.temperature_reading = temperature_reading
        self.needs_clarification = needs_clarification

    def to_dict(self) -> Dict:
        return {
            "original_text": self.original_text,
            "detected_symptoms": self.detected_symptoms,
            "negated_symptoms": self.negated_symptoms,
            "timeline": self.timeline,
            "severity_cue": self.severity_cue,
            "temperature_reading": self.temperature_reading,
            "needs_clarification": self.needs_clarification,
        }


class SymptomNormalizer:
    def __init__(self):
        # Pre-compile expression patterns for performance and boundary detection
        self.negation_pattern = re.compile(
            r"\b(" + "|".join(re.escape(w) for w in NEGATION_WORDS) + r")\b",
            re.IGNORECASE,
        )

        # Timeline regex patterns (e.g. "2 days", "3 din se", "kal raat se", "since yesterday")
        self.timeline_regexes = [
            re.compile(r"(\d+\s*(?:day|days|din|hafte|week|weeks|hours|ghante|mahine|months))\s*(?:se|ago|se chal raha)?", re.IGNORECASE),
            re.compile(r"\b(kal raat se|kal se|aaj subah se|since yesterday|since morning|few days|kuch dino se)\b", re.IGNORECASE),
            re.compile(r"\b(1|2|3|4|5|6|7|8|9|10)\s*(?:din|days)\b", re.IGNORECASE),
        ]

        # Temperature regex patterns (e.g. "102 f", "101.4", "103 degree", "99.5")
        self.temp_regex = re.compile(
            r"\b(9[89]|10[0-6])(?:\.[0-9])?\s*(?:f|c|degree|degrees|deg)?\b",
            re.IGNORECASE,
        )

        # Severity cues
        self.severity_map = {
            "severe": ["severe", "tez", "bahut tez", "bohot tez", "unbearable", "bahut zyada", "extreme", "भयंकर", "अत्यधिक"],
            "moderate": ["moderate", "theek thaak", "beech ka", "medium", "मध्यम"],
            "mild": ["mild", "halka", "halka fulka", "thoda thoda", "slight", "हल्का"],
        }

    def normalize(self, text: str) -> NormalizedExtraction:
        text_clean = text.strip()
        text_lower = text_clean.lower()

        detected: Set[str] = set()
        negated: Set[str] = set()

        # Split text into clauses by punctuation and connectives
        clauses = re.split(r"[,;।\.\n]|(\blekin\b|\bparantu\b|\bbut\b|\baur\b|\band\b)", text_clean, flags=re.IGNORECASE)
        clauses = [c.strip() for c in clauses if c and c.strip()]

        for clause in clauses:
            clause_lower = clause.lower()
            clause_has_negation = bool(self.negation_pattern.search(clause_lower))

            for canonical_sym, expressions in SYMPTOM_EXPRESSIONS.items():
                matched = False
                for expr in expressions:
                    pattern = r"(?<!\w)" + re.escape(expr) + r"(?!\w)"
                    if re.search(pattern, clause_lower):
                        matched = True
                        break

                if matched:
                    if clause_has_negation:
                        negated.add(canonical_sym)
                    else:
                        detected.add(canonical_sym)

        # Negation takes strict precedence if marked in the same context
        active_symptoms = [s for s in detected if s not in negated]
        negated_symptoms_list = list(negated)

        # Extract timeline
        timeline = None
        for regex in self.timeline_regexes:
            match = regex.search(text_lower)
            if match:
                timeline = match.group(0).strip()
                break

        # Extract temperature
        temp_reading = None
        temp_match = self.temp_regex.search(text_lower)
        if temp_match and any(w in text_lower for w in ["fever", "bukhar", "temperature", "temp", "naapa"]):
            temp_reading = temp_match.group(0).strip()

        # Extract severity
        severity_cue = None
        for sev_level, keywords in self.severity_map.items():
            for kw in keywords:
                if re.search(r"(?<!\w)" + re.escape(kw) + r"(?!\w)", text_lower):
                    severity_cue = sev_level
                    break
            if severity_cue:
                break

        # Check for ambiguity: if user provided non-empty input but no symptoms detected
        needs_clarification = len(active_symptoms) == 0 and len(text_clean.split()) > 2 and len(negated_symptoms_list) == 0

        return NormalizedExtraction(
            original_text=text_clean,
            detected_symptoms=active_symptoms,
            negated_symptoms=negated_symptoms_list,
            timeline=timeline,
            severity_cue=severity_cue,
            temperature_reading=temp_reading,
            needs_clarification=needs_clarification,
        )

    def determine_primary_pathway(self, symptoms: List[str]) -> str:
        """Determines the most appropriate conversation pathway based on canonical symptoms."""
        if FEVER in symptoms:
            return FEVER
        elif COUGH in symptoms:
            return COUGH
        elif HEADACHE in symptoms:
            return HEADACHE
        elif ABDOMINAL_PAIN in symptoms:
            return ABDOMINAL_PAIN
        return "general"


symptom_normalizer = SymptomNormalizer()
