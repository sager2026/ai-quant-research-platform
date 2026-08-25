from app.application.services.research_supervisor import (
    ResearchSupervisor,
)

from app.infrastructure.llm.ollama_provider import (
    OllamaProvider,
)


# ---------------------------------------------------------
# 1. LLM
# ---------------------------------------------------------

llm = OllamaProvider(
    model="qwen3:8b"
)


# ---------------------------------------------------------
# 2. Research Supervisor
# ---------------------------------------------------------

supervisor = ResearchSupervisor(
    llm=llm
)


# ---------------------------------------------------------
# 3. Test research questions
# ---------------------------------------------------------

questions = [
    "Is Apple technically oversold?",

    "What are Apple's recent business risks?",

    "What are Apple's long-term structural business risks?",

    (
        "Give me an integrated outlook for Apple using "
        "technical, forecast, and fundamental evidence."
    ),
]


# ---------------------------------------------------------
# 4. Generate and inspect ResearchPlans
# ---------------------------------------------------------

for index, question in enumerate(
    questions,
    start=1,
):

    print()
    print("=" * 70)
    print(f"Test #{index}")
    print(f"Question: {question}")
    print("-" * 70)

    plan = supervisor.plan(
        ticker="AAPL",
        research_question=question,
    )

    print(
        f"use_technical:   "
        f"{plan.use_technical}"
    )

    print(
        f"use_forecast:    "
        f"{plan.use_forecast}"
    )

    print(
        f"use_fundamental: "
        f"{plan.use_fundamental}"
    )

    print(
        f"filing_types:    "
        f"{plan.filing_types}"
    )