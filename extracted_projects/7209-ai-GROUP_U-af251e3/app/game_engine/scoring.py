def calculate_score(answers, correct_answers):
    score = sum([a==b for a,b in zip(answers, correct_answers)])
    return score
