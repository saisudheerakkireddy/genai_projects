def get_questions_for_level(level, topic):
    """Return a list of questions for the given level."""
    return [f"Level {level} question {i} for {topic}" for i in range(1, 4)]
