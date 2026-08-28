import json

from app.application.llm.llm_interface import LLMInterface
from app.domain.entities.fundamental_agent_result import (
    FundamentalAgentResult,
)
from app.domain.entities.retrieval_result import (
    RetrievalResult,
)


class FundamentalResearchAgent:
    """
    Specialized research agent responsible for interpreting
    already-retrieved SEC filing evidence.
    """

    def __init__(
        self,
        llm: LLMInterface,
    ):
        self.llm = llm

    def analyze(
        self,
        ticker: str,
        research_question: str,
        retrieval: RetrievalResult,
    ) -> FundamentalAgentResult:

        # ---------------------------------------------------------
        # 1. Build grounded reasoning prompt
        # ---------------------------------------------------------

        prompt = self._build_prompt(
            ticker=ticker,
            research_question=research_question,
            retrieval=retrieval,
        )

        # ---------------------------------------------------------
        # 2. Ask specialist LLM to interpret evidence
        # ---------------------------------------------------------

        response = self.llm.generate(
            prompt
        )

        # ---------------------------------------------------------
        # 3. Convert LLM output into structured result
        # ---------------------------------------------------------

        return self._parse_response(
            response=response,
            evidence_count=len(
                retrieval.evidence
            ),
        )

    @staticmethod
    def _build_prompt(
        ticker: str,
        research_question: str,
        retrieval: RetrievalResult,
    ) -> str:

        if retrieval.evidence:

            evidence_text = "\n\n".join(
                (
                    f"Evidence #{index}\n"
                    f"Ticker: {evidence.ticker}\n"
                    f"Filing type: {evidence.filing_type}\n"
                    f"Filing date: {evidence.filing_date}\n"
                    f"Section: {evidence.section}\n"
                    f"Source: {evidence.source}\n"
                    f"Text:\n{evidence.text}"
                )
                for index, evidence in enumerate(
                    retrieval.evidence,
                    start=1,
                )
            )

        else:
            evidence_text = (
                "No SEC filing evidence was retrieved."
            )

        return f"""
You are the Fundamental Research Agent in a multi-agent
equity research system.

Your responsibility is to answer the research question
using ONLY the SEC filing evidence supplied below.

Do not use external knowledge.
Do not invent company facts.
Do not invent management actions.
Do not make investment recommendations.

Ticker:
{ticker}

Research question:
{research_question}


SEC FILING EVIDENCE

{evidence_text}


ANALYSIS RULES

1. Use only the supplied SEC filing evidence.

2. Every material observation or risk must be supported
   by at least one supplied Evidence #.

3. Do not invent facts that are not explicitly supported
   by the evidence.

4. Do not infer management actions, mitigation strategies,
   financial impacts, or causal relationships unless the
   supplied evidence supports them.

5. Distinguish company disclosures from your interpretation.

6. Do not claim that a risk will occur merely because
   the filing identifies it as a risk.

7. Do not convert forward-looking risk disclosures into
   predictions of future outcomes.

8. Keep different filing dates and filing types conceptually
   distinct when relevant.

9. Answer the research question directly when the supplied
   evidence supports an answer.

10. If the evidence is insufficient to answer the question,
    state that limitation clearly.

11. evidence_references must contain ONLY integer Evidence #
    values that actually appear in the supplied evidence.

12. Include only evidence references that materially support
    the summary, observations, or risks.


OUTPUT FORMAT

Return ONLY valid JSON.

Do not use Markdown.
Do not include ```json code fences.
Do not include any text before or after the JSON.

Use exactly this structure:

{{
    "summary": "concise evidence-grounded fundamental interpretation",
    "observations": [
        "observation 1",
        "observation 2"
    ],
    "risks": [
        "risk or limitation 1",
        "risk or limitation 2"
    ],
    "evidence_references": [
        1,
        2
    ]
}}
"""

    @staticmethod
    def _parse_response(
        response: str,
        evidence_count: int,
    ) -> FundamentalAgentResult:

        cleaned = response.strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix(
                "```json"
            )
            cleaned = cleaned.removeprefix(
                "```"
            )

            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]

            cleaned = cleaned.strip()

        try:
            data = json.loads(
                cleaned
            )
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Fundamental Research Agent returned "
                "invalid JSON."
            ) from exc

        summary = data.get(
            "summary",
            "",
        )

        observations = data.get(
            "observations",
            [],
        )

        risks = data.get(
            "risks",
            [],
        )

        evidence_references = data.get(
            "evidence_references",
            [],
        )

        if not isinstance(summary, str):
            raise ValueError(
                "Fundamental agent summary must be a string."
            )

        if not isinstance(observations, list):
            raise ValueError(
                "Fundamental agent observations must be a list."
            )

        if not isinstance(risks, list):
            raise ValueError(
                "Fundamental agent risks must be a list."
            )

        if not isinstance(
            evidence_references,
            list,
        ):
            raise ValueError(
                "Fundamental agent evidence references "
                "must be a list."
            )

        validated_references = []

        for reference in evidence_references:

            if not isinstance(reference, int):
                raise ValueError(
                    "Fundamental agent evidence references "
                    "must contain integers."
                )

            if not (
                1
                <= reference
                <= evidence_count
            ):
                raise ValueError(
                    "Fundamental agent referenced an "
                    "unknown Evidence #."
                )

            if reference not in validated_references:
                validated_references.append(
                    reference
                )

        return FundamentalAgentResult(
            summary=summary,
            observations=[
                str(item)
                for item in observations
            ],
            risks=[
                str(item)
                for item in risks
            ],
            evidence_references=validated_references,
        )