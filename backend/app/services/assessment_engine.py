"""Assessment generation engine producing structured, non-prescriptive clinical summaries."""

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
        timeline = collected_data.get("timeline") or "Timeline not specified"

        # Formulate non-diagnostic potential outpatient clinical considerations
        explanations = self._determine_potential_explanations(pathway, detected_symptoms, collected_data)

        # Identify missing or uncertain items
        missing_info = []
        if not collected_data.get("timeline"):
            missing_info.append("Exact onset duration and progression timeline")
        if pathway == PATHWAY_FEVER and not collected_data.get("temperature_reading"):
            missing_info.append("Specific thermometer temperature reading")
        if pathway == PATHWAY_HEADACHE and "headache_location" not in collected_data:
            missing_info.append("Exact anatomical distribution of head pain")
        if pathway == PATHWAY_ABDOMINAL_PAIN and "abdominal_location" not in collected_data:
            missing_info.append("Localized quadrant of abdominal discomfort")

        # Formulate cautious next steps
        next_steps = self._formulate_next_steps(pathway, is_escalated)

        return AssessmentResponse(
            main_concern=chief_complaint or "General Health Assessment",
            reported_symptoms=detected_symptoms if detected_symptoms else ["Unspecified symptoms"],
            duration_timeline=timeline,
            follow_up_summary=follow_up_answers,
            missing_or_uncertain_info=missing_info,
            potential_explanations=explanations,
            warning_signs_screened=[
                "Severe respiratory distress",
                "Acute cardiac chest pressure",
                "FAST neurological stroke signs",
                "Sudden loss of consciousness",
                "Severe hemorrhage or hemoptysis",
                "Severe acute rigid abdomen",
            ],
            red_flags_identified=red_flags_identified,
            is_escalated=is_escalated,
            suggested_next_steps=next_steps,
            professional_consultation_recommended=True,
        )

    def _determine_potential_explanations(
        self,
        pathway: str,
        symptoms: List[str],
        collected_data: Dict[str, Any],
    ) -> List[ClinicalExplanation]:
        explanations: List[ClinicalExplanation] = []

        if pathway == PATHWAY_FEVER:
            explanations.append(
                ClinicalExplanation(
                    title="Acute Viral Syndrome / Seasonal Viral Infection",
                    reasoning="Your reported fever with constitutional symptoms is commonly seen in acute self-limiting viral illnesses.",
                    likelihood_context="Frequent presentation in outpatient settings",
                )
            )
            if "body_pain" in symptoms or "headache" in symptoms:
                explanations.append(
                    ClinicalExplanation(
                        title="Vector-Borne or Endemic Febrile Illness (e.g. Dengue / Chikungunya differential)",
                        reasoning="Fever accompanied by generalized myalgia and headache warrants clinical platelet and CBC monitoring in endemic regions.",
                        likelihood_context="Requires formal laboratory exclusion if high grade",
                    )
                )

        elif pathway == PATHWAY_COUGH:
            explanations.append(
                ClinicalExplanation(
                    title="Upper Respiratory Tract Irritation / Post-Viral Bronchial Sensitivity",
                    reasoning="Cough symptoms commonly reflect upper airway mucosal inflammation following viral exposure or environmental allergens.",
                    likelihood_context="Common acute presentation",
                )
            )
            explanations.append(
                ClinicalExplanation(
                    title="Allergic Bronchitis or Environmental Pharyngitis",
                    reasoning="Airway hyperreactivity from dust, dry air, or seasonal changes can trigger prolonged dry hacking coughs.",
                    likelihood_context="Consider if cough is non-productive without high fever",
                )
            )

        elif pathway == PATHWAY_HEADACHE:
            explanations.append(
                ClinicalExplanation(
                    title="Tension-Type Headache or Eye Strain",
                    reasoning="Gradual onset bilateral or generalized head tightness is frequently linked with fatigue, poor sleep, screen time, or dehydration.",
                    likelihood_context="Most common primary headache type",
                )
            )
            explanations.append(
                ClinicalExplanation(
                    title="Migraine without Aura Consideration",
                    reasoning="Headaches associated with light sensitivity, nausea, or unilateral throbbing may point toward a migrainous pattern.",
                    likelihood_context="Requires clinical neurological assessment if recurrent",
                )
            )

        elif pathway == PATHWAY_ABDOMINAL_PAIN:
            explanations.append(
                ClinicalExplanation(
                    title="Functional Dyspepsia / Acute Gastric Irritation",
                    reasoning="Epigastric discomfort or burning following meals is frequently attributed to hyperacidity or mild gastritis.",
                    likelihood_context="Common outpatient digestive symptom",
                )
            )
            explanations.append(
                ClinicalExplanation(
                    title="Gastroenteritis or Dietary Intolerance",
                    reasoning="Cramping with changes in bowel habits or mild nausea can indicate transient intestinal irritation.",
                    likelihood_context="Self-monitoring recommended alongside hydration",
                )
            )

        else:
            explanations.append(
                ClinicalExplanation(
                    title="Non-Specific Outpatient Symptom Cluster",
                    reasoning="Your reported symptoms do not fall strictly into a single acute syndrome and require in-person physician history taking.",
                    likelihood_context="General clinical review recommended",
                )
            )

        return explanations

    def _formulate_next_steps(self, pathway: str, is_escalated: bool) -> List[str]:
        if is_escalated:
            return [
                "URGENT: Call 112 or local emergency ambulance (108 in India) immediately.",
                "Proceed to the emergency department of the nearest hospital.",
                "Do not drive yourself; seek assistance from family, neighbors, or emergency personnel.",
                "Avoid unprescribed medications or self-treatment in emergency situations.",
            ]

        steps = [
            "Schedule an evaluation with a General Physician for clinical examination and proper diagnosis.",
            "Maintain adequate oral hydration (boiled or filtered water, electrolytes if tolerated).",
            "Get sufficient physical rest and avoid intense exertion while symptoms persist.",
            "Monitor for any new warning signs (such as high unyielding fever, shortness of breath, or severe pain).",
            "If any emergency red flags develop, do not wait — visit an emergency center or call 112 immediately.",
        ]
        return steps


assessment_engine = AssessmentEngine()
