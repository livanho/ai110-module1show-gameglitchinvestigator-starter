import ast
from pathlib import Path

from logic_utils import check_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result[0] == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result[0] == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result[0] == "Too Low"


def test_attempts_initialization_consistent_with_new_game():
    app_path = Path(__file__).resolve().parents[1] / "app.py"
    tree = ast.parse(app_path.read_text(encoding="utf-8"))

    init_attempts_zero = False
    new_game_attempts_zero = False

    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue

        test = node.test

        # First-load path: if "attempts" not in st.session_state:
        if isinstance(test, ast.Compare):
            left_is_attempts = isinstance(test.left, ast.Constant) and test.left.value == "attempts"
            has_not_in = len(test.ops) == 1 and isinstance(test.ops[0], ast.NotIn)
            if left_is_attempts and has_not_in:
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Constant) and stmt.value.value == 0:
                        if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Attribute):
                            target = stmt.targets[0]
                            if target.attr == "attempts":
                                init_attempts_zero = True

        # New-game path: if new_game:
        if isinstance(test, ast.Name) and test.id == "new_game":
            for stmt in node.body:
                if isinstance(stmt, ast.Assign) and isinstance(stmt.value, ast.Constant) and stmt.value.value == 0:
                    if len(stmt.targets) == 1 and isinstance(stmt.targets[0], ast.Attribute):
                        target = stmt.targets[0]
                        if target.attr == "attempts":
                            new_game_attempts_zero = True

    assert init_attempts_zero
    assert new_game_attempts_zero


def test_hint_messages_match_outcome_labels_in_check_guess():
    """Regression test: Too High must say LOWER, Too Low must say HIGHER."""
    logic_utils_path = Path(__file__).resolve().parents[1] / "logic_utils.py"
    tree = ast.parse(logic_utils_path.read_text(encoding="utf-8"))

    too_high_has_lower_hint = False
    too_low_has_higher_hint = False

    for node in ast.walk(tree):
        if not isinstance(node, ast.Return) or not isinstance(node.value, ast.Tuple):
            continue

        elts = node.value.elts
        if len(elts) != 2:
            continue

        outcome_node, hint_node = elts
        if not isinstance(outcome_node, ast.Constant) or not isinstance(hint_node, ast.Constant):
            continue
        if not isinstance(outcome_node.value, str) or not isinstance(hint_node.value, str):
            continue

        if outcome_node.value == "Too High" and "LOWER" in hint_node.value:
            too_high_has_lower_hint = True
        if outcome_node.value == "Too Low" and "HIGHER" in hint_node.value:
            too_low_has_higher_hint = True

    assert too_high_has_lower_hint
    assert too_low_has_higher_hint
