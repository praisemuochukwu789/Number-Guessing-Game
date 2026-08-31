import json
from pathlib import Path
import random
import time

HIGHSCORE_FILE = Path("highscores.json")


def load_high_scores():
    """Reads high scores from the JSON file or returns default empty structure."""
    if not HIGHSCORE_FILE.exists():
        return {"Easy": None, "Medium": None, "Hard": None}

    try:
        with open(HIGHSCORE_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {"Easy": None, "Medium": None, "Hard": None}


def save_high_score(difficulty, attempts, time_taken):
    """Updates and saves the high score for a specific difficulty if it's a new record."""
    scores = load_high_scores()
    current_best = scores.get(difficulty)

    is_new_record = False
    if current_best is None:
        is_new_record = True
    elif attempts < current_best["attempts"]:
        is_new_record = True
    elif attempts == current_best["attempts"] and time_taken < current_best["time"]:
        is_new_record = True

    if is_new_record:
        scores[difficulty] = {"attempts": attempts, "time": time_taken}
        with open(HIGHSCORE_FILE, "w") as file:
            json.dump(scores, file, indent=4)
        print(f"\n🏆 NEW HIGH SCORE for {difficulty} mode! 🏆")


def display_high_scores():
    """Displays current high scores in a clean terminal layout."""
    scores = load_high_scores()
    print("\n========== 🏆 HIGH SCORES 🏆 ==========")
    for level, data in scores.items():
        # prints and format the data using 8 character width
        if data:
            print(f"{level:<8} | Attempts: {data['attempts']} | Time: {data['time']}s")
        else:
            print(f"{level:<8} | No record yet")
    print("========================================")


def select_difficulty():
    """Prompts the user to select a difficulty level and returns the name and chances."""
    print("\nPlease select the difficulty level:")
    print("1. Easy (20 chances)")
    print("2. Medium (15 chances)")
    print("3. Hard (10 chances)")

    levels = {"1": ("Easy", 20), "2": ("Medium", 15), "3": ("Hard", 10)}

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in levels:
            difficulty, chances = levels[choice]
            print(f"\nGreat! You have selected the {difficulty} level.")
            print("Let's start the game!")
            return difficulty, chances
        print("Invalid choice. Please enter 1, 2, or 3.")


def play_round():
    """Runs a single round of the Number Guessing Game."""
    target_number = random.randint(1, 100)
    difficulty, chances = select_difficulty()

    attempts = 0
    start_time = time.time()

    while attempts < chances:
        attempts += 1
        remaining = chances - attempts

        try:
            guess = int(input("\nEnter your guess: "))
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            attempts -= 1 # reverse invalid attempts
            continue

        if guess == target_number:
            time_taken = round(time.time() - start_time, 2) # round to two decimal places
            print(
                f"\nCongratulations! You guessed the correct number in {attempts} attempts!"
            )
            print(f"Time taken: {time_taken} seconds.")

            save_high_score(difficulty, attempts, time_taken)
            return

        if guess < target_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")

        if remaining > 0:
            print(f"Chances remaining: {remaining}")

    print(
        f"\nGame Over! You ran out of chances. The correct number was {target_number}."
    )


def main():
    """Main program entry point with replay loop."""
    print("==================================================")
    print(" Welcome to the Number Guessing Game!")
    print(" I'm thinking of a number between 1 and 100.")
    print("==================================================")

    display_high_scores()

    while True:
        play_round()

        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ("y", "yes"):
            print("\nThanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()