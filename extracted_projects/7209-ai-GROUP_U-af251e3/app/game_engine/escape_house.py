def play_escape_house(questions):
    """Simulate Escape House game flow."""
    print("[Game] Starting Escape House")
    for idx, q in enumerate(questions, 1):
        print(f"Question {idx}: {q}")
        answer = input("Your answer: ")
        print(f"You answered: {answer}")
    print("[Game] All questions answered! You found the password!")
