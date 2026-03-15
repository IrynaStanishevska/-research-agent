from agent import agent


def main():
    print("Research Agent (type 'exit' to quit)")
    print("-" * 40)

    thread_config = {"configurable": {"thread_id": "research-session-1"}}

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                thread_config,
            )

            messages = result.get("messages", [])
            if messages:
                last_message = messages[-1]
                if hasattr(last_message, "content"):
                    print(f"\nAgent: {last_message.content}")
                else:
                    print(f"\nAgent: {last_message}")
            else:
                print("\nAgent: No response returned.")

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    main()