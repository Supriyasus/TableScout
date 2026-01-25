from backend.agents.intent_extraction_agent import IntentExtractionAgent

def main():
    agent = IntentExtractionAgent()

    intent = agent.extract(
        "Show me a calm cozy place with amazing food, not too crowded"
    )

    print("---- Extracted Intent ----")
    print(intent.model_dump())

if __name__ == "__main__":
    main()
