import random
import time


def select_difficulty():
    """Prompts the user to select a difficulty level and returns the allowed chances."""
    print("\nPlease select the difficulty level:")
    print("1. Easy (10 chances)")
    print("2. Medium (5 chances)")
    print("3. Hard (3 chances)")

    levels = {"1": ("Easy", 20), "2": ("Medium", 15), "3": ("Hard", 10)}

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in levels:
            name, chances = levels[choice]
            print(f"\nGreat! You have selected the {name} difficulty level.")
            print("Let's start the game!")
            return name, chances
        print("Invalid choice. Please enter 1, 2, or 3.")


def play_round():
    """Runs a single round of the Number Guessing Game."""
    target_number = random.randint(1, 100)
    chances = select_difficulty()

    attempts = 0
    start_time = time.time()

    while attempts < chances:
        attempts += 1
        remaining = chances - attempts

        try:
            guess = int(input("\nEnter your guess: "))
        except ValueError:
            print("Invalid input! Please enter a valid integer.")
            attempts -= 1  # Don't penalize invalid input
            continue

        if guess == target_number:
            elapsed_time = round(time.time() - start_time, 2)
            print(
                f"\nCongratulations! You guessed the correct number in {attempts} attempts!"
            )
            print(f"Time taken: {elapsed_time} seconds.")
            return

        if guess < target_number:
            print(f"Incorrect! The number is greater than {guess}.")
        else:
            print(f"Incorrect! The number is less than {guess}.")

        if remaining > 0:
            print(f"Chances remaining: {remaining}")

    print(f"\nGame Over! You ran out of chances. The correct number was {target_number}.")


def main():
    """Main program entry point with replay loop."""
    print("==================================================")
    print(" Welcome to the Number Guessing Game!")
    print(" I'm thinking of a number between 1 and 100.")
    print("==================================================")

    while True:
        play_round()

        play_again = input("\nDo you want to play again? (y/n): ").strip().lower()
        if play_again not in ("y", "yes"):
            print("\nThanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()