import goals_engine


def test_match_goal_math():
    goals = goals_engine.load_goals()
    matches = goals_engine.match_goal("I need help with math homework", goals)
    names = [m[0] for m in matches]
    assert "high_school_support" in names or "education" in names


def test_match_goal_menstruation():
    goals = goals_engine.load_goals()
    matches = goals_engine.match_goal("What is menstruation?", goals)
    names = [m[0] for m in matches]
    assert "women's_health" in names


def test_match_goal_constitution():
    goals = goals_engine.load_goals()
    matches = goals_engine.match_goal("What are my constitutional rights?", goals)
    names = [m[0] for m in matches]
    assert "constitutional_rights" in names or "justice" in names
