# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

- Bug: Secret number type flipped between int and str on alternating attempts.
  - Expected: The secret number should remain a numeric value (int) for the
    whole game so numeric comparisons behave predictably.
  - Actual: On every even attempt the code converts the secret to a string
    (so comparisons fall back to lexicographic string comparison). This
    produced surprising results like `9` comparing greater than `10` and
    caused the `TypeError` fallback branch to run intermittently.

- Bug: Hint messages are inverted relative to the outcome labels.
  - Expected: When the outcome is "Too High" the hint should instruct the
    player to go lower, and when "Too Low" the hint should instruct them to
    go higher.
  - Actual: The app returns "Too High" paired with the message "📈 Go HIGHER!"
    and "Too Low" with "📉 Go LOWER!", which is misleading and actively
    contradicts the outcome label.

- Bug: Difficulty range and new-game behavior are inconsistent.
  - Expected: The displayed range, the secret generation, and the new-game
    action should all respect the difficulty selected via `get_range_for_difficulty`.
  - Actual: The info text always says "between 1 and 100", and the New Game
    button creates a secret with `random.randint(1, 100)` regardless of the
    chosen difficulty, so the secret's range can mismatch the selected difficulty.

- Bug: `attempts` initialization is inconsistent between first load and new-game.
  - Expected: The attempt counter should have a single consistent starting
    value (usually 0 or 1) and behave predictably after starting a new game.
  - Actual: On first load `attempts` is initialized to `1`, but the New Game
    button sets `attempts = 0`, creating off-by-one confusion in UI text and
    scoring that depends on attempt parity.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used GitHub Copilot as my main AI teammate during this project. I asked it to make a focused refactor, moving `check_guess` from `app.py` into `logic_utils.py`, and to update imports with minimal side effects. That suggestion was correct because the code compiled, the import path worked, and after targeted updates the test suite passed (`5 passed`).

One misleading part was the initial assumption that only moving the function would be enough without touching tests. After the refactor, tests that inspected `app.py` for `check_guess` behavior failed, and a few assertions expected a string instead of the tuple returned by the function. I verified that mismatch by running pytest, reading the failure messages, and then fixing only refactor-related tests so they pointed to `logic_utils.py` and checked the correct return shape.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I treated a bug as fixed only when both behavior and tests matched the intended result. I used `pytest -q` after each targeted change instead of assuming a refactor was safe just because the app still ran. One concrete example was the `check_guess` refactor: the first test run failed, which showed the tests were coupled to the old function location and expected return shape. After updating only refactor-related tests, a second run showed `5 passed`, which confirmed the move was clean. AI helped by surfacing the exact failure patterns quickly, and I used those failures to guide small, focused fixes.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit I want to keep is making one small change at a time and running tests immediately after each change. It made debugging faster because I could tie failures to a specific edit instead of guessing across many changes. Next time, I would ask AI up front to identify test files likely affected by a refactor so I can update them in the same pass. This project changed how I view AI-generated code: it is a strong accelerator, but I treat every suggestion as a draft that still needs verification through tests and code review.
