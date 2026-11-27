"""Questioning engine managing follow-up clinical dialogue progression.
Enforces a maximum of 4 targeted questions and skips already answered inquiries.
"""

from typing import Dict, List, Optional, Any, Tuple
from app.medical_data.question_flows import QUESTION_FLOWS, PATHWAY_GENERAL
from app.schemas.conversation import QuestionDetail


class QuestioningEngine:
    MAX_QUESTIONS = 4

    def get_next_question(
        self,
        pathway: str,
        asked_question_ids: List[str],
        collected_data: Dict[str, Any],
        language: str = "hinglish",
    ) -> Optional[QuestionDetail]:
        """Selects the next relevant clinical follow-up question.
        Returns None if maximum questions reached or all relevant questions answered.
        """
        if len(asked_question_ids) >= self.MAX_QUESTIONS:
            return None

        flow = QUESTION_FLOWS.get(pathway, QUESTION_FLOWS[PATHWAY_GENERAL])

        for q in flow:
            q_id = q["id"]

            # Skip if already asked
            if q_id in asked_question_ids:
                continue

            # Skip if entity answer was already supplied in initial or previous messages
            skip_entities = q.get("skip_if_entities", [])
            already_answered = False
            for entity in skip_entities:
                if entity in collected_data and collected_data[entity]:
                    already_answered = True
                    break

            if already_answered:
                continue

            # Found next question to ask
            if language == "hi":
                q_text = q["question_hi"]
            elif language == "en":
                q_text = q["question_en"]
            else:
                q_text = q["question_hinglish"]

            current_index = len(asked_question_ids) + 1
            return QuestionDetail(
                id=q_id,
                key=q["key"],
                text=q_text,
                category=q["category"],
                question_index=current_index,
                total_questions=self.MAX_QUESTIONS,
            )

        return None


questioning_engine = QuestioningEngine()
