from chatbot import load_all_documents, chatbot_answer


def main():
    documents = load_all_documents()

    if not documents:
        print("No documents loaded. Exiting.")
        return

    print("📘 Chatbot ready.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        question = input("> ")

        if question.lower() in ("exit", "quit"):
            print("Goodbye.")
            break

        answer = chatbot_answer(question, documents)
        print("\n" + answer + "\n")


if __name__ == "__main__":
    main()
