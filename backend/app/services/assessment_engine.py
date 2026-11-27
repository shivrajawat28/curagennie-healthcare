"""Assessment generation engine producing structured, non-prescriptive clinical summaries.
Strictly audited to prevent unsupported diagnoses, invented probabilities, or false reassurance.
"""

from typing import Dict, List, Any, Optional
from app.schemas.assessment import AssessmentResponse, ClinicalExplanation
from app.medical_data.question_flows import (
    PATHWAY_FEVER,
    PATHWAY_COUGH,
    PATHWAY_HEADACHE,
    PATHWAY_ABDOMINAL_PAIN,
)


class AssessmentEngine:
    def generate_assessment(
        self,
        chief_complaint: str,
        pathway: str,
        detected_symptoms: List[str],
        collected_data: Dict[str, Any],
        follow_up_answers: Dict[str, str],
        red_flags_identified: List[str],
        is_escalated: bool = False,
    ) -> AssessmentResponse:
        timeline = collected_data.get("timeline") or "Timeline not specified by patient"

        # Explicitly separate patient-reported factual data
        user_facts: Dict[str, Any] = {
            "chief_complaint": chief_complaint,
            "reported_symptoms": detected_symptoms if detected_symptoms else ["Unspecified symptoms"],
            "timeline": timeline,
            "measured_temperature": collected_data.get("temperature_reading"),
            "severity_cue": collected_data.get("severity_cue"),
            "follow_up_responses": follow_up_answers,
        }

        # Formulate non-diagnostic potential outpatient clinical considerations
        explanations, interpretation_summary = self._determine_potential_explanations(
            pathway, detected_symptoms, collected_data, follow_up_answers, is_escalated
        )

        # Identify missing or uncertain clinical items
        missing_info: List[str] = []
        if not collected_data.get("timeline"):
            missing_info.append("Exact onset duration and daily progression pattern")
        if pathway == PATHWAY_FEVER and not collected_data.get("temperature_reading"):
            missing_info.append("Objective thermometer temperature measurement (fever grade unconfirmed)")
        if pathway == PATHWAY_HEADACHE and "headache_location" not in collected_data:
            missing_info.append("Detailed anatomical pain mapping (unilateral vs bilateral vs frontal)")
        if pathway == PATHWAY_ABDOMINAL_PAIN:
            missing_info.append("Physical abdominal palpation and localized tenderness assessment (cannot be performed online)")

        # Formulate cautious next steps
        next_steps = self._formulate_next_steps(pathway, is_escalated)

        return AssessmentResponse(
            main_concern=chief_complaint or "General Health Assessment",
            reported_symptoms=detected_symptoms if detected_symptoms else ["Unspecified symptoms"],
            duration_timeline=timeline,
            follow_up_summary=follow_up_answers,
            user_reported_facts=user_facts,
            clinical_interpretations_summary=interpretation_summary,
            missing_or_uncertain_info=missing_info,
            potential_explanations=explanations,
            warning_signs_screened=[
                "Severe respiratory distress / cyanosis",
                "Acute cardiac chest pressure radiating to arm or jaw",
                "FAST neurological stroke signs (face droop, arm weakness, slurred speech)",
                "Sudden loss of consciousness or syncope",
                "Severe hemorrhage or hemoptysis",
                "Severe acute rigid board-like abdomen",
            ],
            red_flags_identified=red_flags_identified,
            is_escalated=is_escalated,
            suggested_next_steps=next_steps,
            professional_consultation_recommended=True,
            disclaimer=(
                "This health summary is an educational triage guide and not a confirmed medical diagnosis or prescription. "
                "CuraGennie does not prescribe medications. Always consult a qualified physician for clinical evaluation."
            ),
        )

    def _determine_potential_explanations(
        self,
        pathway: str,
        symptoms: List[str],
        collected_data: Dict[str, Any],
        follow_up_answers: Dict[str, str],
        is_escalated: bool,
    ) -> tuple[List[ClinicalExplanation], str]:
        explanations: List[ClinicalExplanation] = []

        if is_escalated:
            explanations.append(
                ClinicalExplanation(
                    title="Potential Acute Emergency Warning Presentation",
                    reasoning="Your reported symptoms include one or more acute warning signs requiring urgent emergency physical evaluation.",
                    likelihood_context="High urgency - requires immediate in-person triage",
                )
            )
            summary = "Acute warning signs detected. Routine non-emergency assessment suspended. Immediate emergency care advised."
            return explanations, summary

        # Check if only a single isolated nonspecific symptom is reported without supportive details
        has_multiple_features = len(symptoms) > 1 or bool(collected_data.get("timeline")) or bool(follow_up_answers)

        if not has_multiple_features:
            explanations.append(
                ClinicalExplanation(
                    title="Undifferentiated Outpatient Symptom Presentation",
                    reasoning="A single isolated symptom without duration, severity context, or associated clinical markers is nonspecific and can have numerous common origins. In-person clinical history taking is required.",
                    likelihood_context="Undifferentiated - requires physical physician review",
                )
            )
            summary = (
                "Your reported symptom is currently undifferentiated. A single symptom without timeline or associated "
                "markers cannot support a specific clinical pattern. Other explanations are possible. This is not a diagnosis."
            )
            return explanations, summary

        # Pathway-specific cautious outpatient considerations
        if pathway == PATHWAY_FEVER:
            explanations.append(
                ClinicalExplanation(
                    title="Acute Viral Syndrome / Febrile Illness Consideration",
                    reasoning="Fever accompanied by constitutional symptoms is commonly observed in acute, self-limiting viral infections.",
                    likelihood_context="Common outpatient presentation; monitor progression",
                )
            )
            # Only mention vector-borne differential if multi-symptom support exists (body pain, chills, or headache)
            if any(s in symptoms for s in ["body_pain", "headache", "chills"]):
                explanations.append(
                    ClinicalExplanation(
                        title="Endemic Febrile Illness Differential (e.g. Vector-Borne Prodrome)",
                        reasoning="In endemic areas, fever accompanied by generalized body aches, headache, or chills warrants clinical monitoring and basic blood counts (CBC) if persistent.",
                        likelihood_context="Differential consideration if fever remains high grade",
                    )
                )

        elif pathway == PATHWAY_COUGH:
            explanations.append(
                ClinicalExplanation(
                    title="Upper Airway / Respiratory Mucosal Irritation",
                    reasoning="Cough symptoms frequently reflect upper respiratory tract inflammation following a common cold, viral exposure, or environmental irritants.",
                    likelihood_context="Common self-monitoring presentation",
                )
            )
            # Check if allergic or persistent dry cough
            if "dry_cough" in symptoms or "throat_pain" in symptoms or "sore_throat" in symptoms:
                explanations.append(
                    ClinicalExplanation(
                        title="Post-Viral Bronchial Sensitivity or Environmental Irritation",
                        reasoning="Dry or scratchy coughs may persist following airway hyperreactivity to dust, dry air, or seasonal changes.",
                        likelihood_context="Requires clinical evaluation if lasting over 2-3 weeks",
                    )
                )

        elif pathway == PATHWAY_HEADACHE:
            explanations.append(
                ClinicalExplanation(
                    title="Tension-Type Headache or Musculoskeletal Strain Pattern",
                    reasoning="Gradual onset head pressure or tightness is commonly associated with fatigue, insufficient sleep, screen strain, or dehydration.",
                    likelihood_context="Most common primary headache pattern in outpatients",
                )
            )
            # Only consider migrainous features if supported by nausea, vision, or light sensitivity
            if any(s in symptoms for s in ["nausea_vomiting", "dizziness"]) or any("roshni" in v.lower() or "light" in v.lower() for v in follow_up_answers.values()):
                explanations.append(
                    ClinicalExplanation(
                        title="Vascular / Migrainous Pattern Consideration",
                        reasoning="Headaches accompanied by nausea, sensitivity to bright light, or unilateral throbbing may suggest a migrainous pattern.",
                        likelihood_context="Requires formal neurological evaluation if recurrent or disabling",
                    )
                )

        elif pathway == PATHWAY_ABDOMINAL_PAIN:
            explanations.append(
                ClinicalExplanation(
                    title="Functional Dyspepsia / Acute Gastric Irritation",
                    reasoning="Upper abdominal burning or discomfort following meals is frequently attributed to hyperacidity or transient gastritis.",
                    likelihood_context="Common digestive symptom",
                )
            )
            # If cramping or accompanied by nausea / loose motions
            if "diarrhea" in symptoms or "nausea_vomiting" in symptoms or any("marod" in v.lower() or "cramp" in v.lower() for v in follow_up_answers.values()):
                explanations.append(
                    ClinicalExplanation(
                        title="Gastrointestinal Irritation or Dietary Indiscretion",
                        reasoning="Cramping accompanied by nausea or bowel habit changes can indicate transient gastrointestinal upset.",
                        likelihood_context="Requires hydration and physician review if prolonged",
                    )
                )

        else:
            explanations.append(
                ClinicalExplanation(
                    title="General Outpatient Symptom Cluster",
                    reasoning="Your reported symptoms do not fall strictly into a single acute syndrome and require in-person history taking and examination.",
                    likelihood_context="General clinical review recommended",
                )
            )

        summary = (
            "Your reported symptoms may be consistent with common outpatient presentations. "
            "Other explanations are possible. This is educational guidance, not a confirmed diagnosis or prescription."
        )
        return explanations, summary

    def _formulate_next_steps(self, pathway: str, is_escalated: bool) -> List[str]:
        if is_escalated:
            return [
                "URGENT: Call 112 (National Emergency Helpline) or local ambulance (108 in India) immediately.",
                "Proceed without delay to the nearest hospital emergency department.",
                "Do not drive yourself; seek immediate assistance from emergency services or family.",
                "Do not consume self-administered medications during acute emergency symptoms.",
            ]

        steps = [
            "Schedule an appointment with a General Physician for formal physical examination.",
            "Maintain adequate oral hydration (drink clean, filtered water, ORS or clear fluids as tolerated).",
            "Prioritize physical rest and avoid heavy exertion while symptoms are active.",
            "Monitor your symptoms closely; note any new developments or worsening intensity.",
            "Seek emergency care immediately (dial 112) if red-flag signs appear (such as chest tightness, difficulty breathing, or severe sudden pain).",
        ]
        return steps


assessment_engine = AssessmentEngine()
