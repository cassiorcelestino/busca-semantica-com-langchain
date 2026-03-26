from search import search_prompt


def main():

    print ("=" * 50)
    print("Chat iniciado. Digite uma pergunta ou 'sair' para encerrar.")

    while True:
        question = input("PERGUNTA: ").strip()

        if question.lower() == "sair":
            print("Encerrando chat.")
            break

        if not question:
            print("Digite uma pergunta valida.")
            continue

        search_data = search_prompt(question)
        answer = search_data["answer"]

        print(f"RESPOSTA: {answer}")
        print()


if __name__ == "__main__":
    main()
