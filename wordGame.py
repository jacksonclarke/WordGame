# Imports.
# Recieves os info for clear() function.
from os import system, name

# Imports color class.
from pretty import *

# Imports "random" module.
import random

# Local database imports.
import sqlite3
from contextlib import closing

# Imports "easy" "medium" "hard" "extreme" "cheatList" and "words" lists.
from Lists.words import *

# Connect to local database.
connection = sqlite3.connect("users.db")
cursor = connection.cursor()

# Permanent local variables (DO NOT MAKE GLOBAL).
user = ""
newUser = ""
score = 0

# Setting up vairables
color = colorClass()
playagain = "y"
secretWord = ""
letterCount = 0
guess = ""
guess_count = 0
i = 0
hint = []
correct = []
difficulty = ""
newPoints = 0
baseNewPoints = 0
multiplyer = 1
e = False
t = 0

# Functions

# Function for exiting game
def exitGame(tempUser, score):
    global connection
    global cursor
    t = 0
    if tempUser != "guest":
        print("\nThanks for playing! See you again soon!")
        cursor.execute("UPDATE users SET score = ? WHERE name = ?", (score, tempUser))
        connection.commit()
        with closing(sqlite3.connect("users.db")) as connection:
            with closing(connection.cursor()) as cursor:
                print("Game saved!")
        quit()
    else:
        print(f"'Guest' Score : {score}")
        guestfinal = input(
            "You have been playing on 'Guest' mode. Would you liked to create a \
    Username so that your score will be saved(y/n)? "
        )
        if guestfinal[0] == "y":
            target_user = input(f"Please enter your username(Make it unique): ")
            while target_user in allUsers:
                print(f"\nThat username is already taken. Please try again.")
                target_user = input(
                    f"Please enter your username{color.UNDERLINE}(Make it unique){color.END()}: "
                )
                t += 1
                if t >= 8:
                    print(
                        "\nYou have tried to enter a username too many times. Your score was not saved.\n"
                    )
                    user = "guest"
                    break
            if user != "guest":
                cursor.execute(
                    f"INSERT INTO users (name, score) VALUES (?, ?)",
                    (
                        target_user,
                        score,
                    ),
                )
                cursor.execute(
                    "UPDATE users SET score = ? WHERE name = ?", (score, target_user)
                )
                connection.commit()
                with closing(sqlite3.connect("users.db")) as connection:
                    with closing(connection.cursor()) as cursor:
                        print("Game saved!")
            else:
                print("Consider signing up next time!")
                quit()
        else:
            print("Consider signing up next time!")
            quit()


# Sets up secret word depending on user input.
def wordDifficulty():
    secretWord = ""
    global baseNewPoints
    wordDif = input(
        f"\nWhat word difficulty would you like to play on? {color.GREEN()}EASY{color.END()}(10 points),\
 {color.BLUE()}Medium{color.END()}(25 points), \n{color.RED()}Hard{color.END()}(50 points), \
or {color.RED()}{color.BOLD()}EXTREME{color.END()}(100 points)? "
    )
    wordDif = wordDif.lower()
    if wordDif == "easy":
        secretWord = random.choice(easy)
        baseNewPoints = 10
        return secretWord
    elif wordDif == "medium":
        secretWord = random.choice(medium)
        baseNewPoints = 25
        return secretWord
    elif wordDif == "hard":
        secretWord = random.choice(hard)
        baseNewPoints = 50
        return secretWord
    elif wordDif == "extreme":
        secretWord = random.choice(extreme)
        baseNewPoints = 100
        return secretWord
    else:
        secretWord = random.choice(words)
        baseNewPoints = 15
        return secretWord


# Sets difficulty and calls wordDifficulty().
def difficultyFunc():
    # Sets difficulty as global and declares global variables.
    global guess_count
    global difficulty
    global secretWord
    global letterCount
    global multiplyer
    global baseNewPoints
    # Asks user for difficulty.
    difficulty = input(
        f"Choose a difficulty level: \n{color.GREEN()}EASY{color.END()} (100 guesses & free hints! No score muliplyer), \n{color.BLUE()}MEDIUM{color.END()}\
(12 guesses & hints|Hints cost 2 points and 1 guess!| Score multiplyer: 2 for each guesses left!), \
\n{color.RED()}HARD{color.END()} (7 guesses |No hints| Score multiplyer: 20 for each guess left!): "
    )
    # Sets difficulty to lowercase.
    difficulty = difficulty.lower()
    # If user chooses easy difficulty.
    if difficulty == "easy":
        # Sets number of guesses to 100.
        guess_count = 100
        multiplyer = 1
        # Sets secret word to wordDifficulty().
        secretWord = wordDifficulty()
        #
        print(color.GREEN())
        print(
            r"""
    █████████████████████████
    █▄─▄▄─██▀▄─██─▄▄▄▄█▄─█─▄█
    ██─▄█▀██─▀─██▄▄▄▄─██▄─▄██
    ▀▄▄▄▄▄▀▄▄▀▄▄▀▄▄▄▄▄▀▀▄▄▄▀▀
        """
        )
        print(color.END())
    # If user chooses medium difficulty.
    elif difficulty == "medium":
        guess_count = 12
        multiplyer = 2
        secretWord = wordDifficulty()
        print(color.BLUE())
        print(
            r"""
    ███╗░░░███╗███████╗██████╗░██╗██╗░░░██╗███╗░░░███╗
    ████╗░████║██╔════╝██╔══██╗██║██║░░░██║████╗░████║
    ██╔████╔██║█████╗░░██║░░██║██║██║░░░██║██╔████╔██║
    ██║╚██╔╝██║██╔══╝░░██║░░██║██║██║░░░██║██║╚██╔╝██║
    ██║░╚═╝░██║███████╗██████╔╝██║╚██████╔╝██║░╚═╝░██║
    ╚═╝░░░░░╚═╝╚══════╝╚═════╝░╚═╝░╚═════╝░╚═╝░░░░░╚═╝
        """
        )
        print(color.END())
    # If user chooses hard difficulty.
    elif difficulty == "hard":
        guess_count = 7
        multiplyer = 20
        secretWord = wordDifficulty()
        print(color.RED())
        print(
            r"""
    .------..------..------..------.
    |H.--. ||A.--. ||R.--. ||D.--. |
    | :/\: || (\/) || :(): || :/\: |
    | (__) || :\/: || ()() || (__) |
    | '--'H|| '--'A|| '--'R|| '--'D|
    `------'`------'`------'`------'
        """
        )
        print(color.END())
    # If user does not correctly enter difficulty.
    else:
        print(
            "\nYou did not choose a valid difficulty level. You will only have 3 guesses as punishment for your mistake."
        )
        print(
            "Oh, and you will be locked on the hardest word difficulty for the rest of the game."
        )
        difficulty = "cheater"
        guess_count = 3
        multiplyer = 1000
        baseNewPoints = 100
        print(
            rf"""{color.RED()}
    ███████████████████████████
    ███████▀▀▀░░░░░░░▀▀▀███████
    ████▀░░░░░░░░░░░░░░░░░▀████
    ███│░░░░░░░░░░░░░░░░░░░│███
    ██▌│░░░░░░░░░░░░░░░░░░░│▐██
    ██░└┐░░░░░░░░░░░░░░░░░┌┘░██
    ██░░└┐░░░░░░░░░░░░░░░┌┘░░██
    ██░░┌┘▄▄▄▄▄░░░░░▄▄▄▄▄└┐░░██
    ██▌░│██████▌░░░▐██████│░▐██
    ███░│▐███▀▀░░▄░░▀▀███▌│░███
    ██▀─┘░░░░░░░▐█▌░░░░░░░└─▀██
    ██▄░░░▄▄▄▓░░▀█▀░░▓▄▄▄░░░▄██
    ████▄─┘██▌░░░░░░░▐██└─▄████
    █████░░▐█─┬┬┬┬┬┬┬─█▌░░█████
    ████▌░░░▀┬┼┼┼┼┼┼┼┬▀░░░▐████
    █████▄░░░└┴┴┴┴┴┴┴┘░░░▄█████
    ███████▄░░░░░░░░░░░▄███████
    ██████████▄▄▄▄▄▄▄██████████
    ███████████████████████████
        """
        )
        print(color.END())
        print(f"{color.RED()}{color.BOLD()}Goodluck{color.END()}\n")
        secretWord = random.choice(extreme)
    letterCount = len(secretWord)


# Checks if letters guessed are in 'correct' list.
def checkCorrectList(letter):
    if letter in secretWord:
        if letter in correct:
            return
        else:
            correct.append(letter)
    else:
        return


# Clears terminal screen.
def clear():

    # For Windows users.
    if name == "nt":
        _ = system("cls")

    # For Mac and Linux(here, os.name is 'posix').
    else:
        _ = system("clear")


# Function to reset variables and lists. Restarts game.
def reset():
    # Runs clear() function.
    clear()
    # Sets variables as global.
    global secretWord
    global letterCount
    global guess
    global guess_count
    global i
    global hint
    global correct
    global letter
    global difficulty
    global newPoints
    # Sets variables to default values.
    secretWord = ""
    guess = ""
    difficulty = ""
    guess_count = 0
    i = 0
    hint = []
    correct = []
    newPoints = 0
    # Tells user the game has restarted.
    print(f"\n{color.GREEN()}The word has been reset!{color.END()}")
    # Displays commands.
    print(
        "\nCommands:\nIf you would like to give up at anytime, type 'giveup'\
    If you would like to see\nthe hint at anytime, and are on Easy or Medium difficulty, type 'hint'\n"
    )
    # Runs difficulty() function.
    difficultyFunc()
    # Updates hint with correct list length
    for letter in secretWord:
        hint.append("_")
    # Displays first hint.
    print(f"Your hint is: " + " ".join(hint) + "\n")


# Game loop starts(line 223) because playagain is set to true.


# Intro message.
print("-" * 50)
print(
    "\nWelcome to the word guessing game!\n\nCommands:\nIf you would like to give up at anytime, type 'giveup'\n\
If you would like to see the hint at anytime, and are on Easy or Medium difficulty, type 'hint'\n"
)
print("-" * 50)

# Sign in and sign up.
newUser = input("Are you a new player? (y/n): ").lower()
if newUser[0] == "y":
    response = input(
        "Would you like to create a Username so that your score will be saved?(y/n): "
    ).lower()
    if response[0] == "y":
        target_user = input(
            f"\nPlease enter your username(Make it unique) \nIf you would like to log in again \
in the future, {color.BOLD()}WRITE IT DOWN!{color.END()}\n Username: "
        ).strip()
        while target_user.lower() == "guest" or target_user.lower() == "":
            print(
                f"{color.RED()}You cannot use the username '{target_user}'{color.END()}"
            )
            target_user = input(
                f"\nPlease enter your username(Make it unique with no spaces) \nIf you would like to log in again \
in the future, {color.BOLD()}WRITE IT DOWN!{color.END()}\nUsername: "
            )
        allUsers = cursor.execute("SELECT name FROM users").fetchall()
        # for user in allUsers:
        #     print(user[0])
        for username in allUsers:
            if username[0] == target_user:
                print(f"\nThat username is already taken. Please try again.")
                target_user = input(
                    f"Please enter your username{color.UNDERLINE()}(Make it unique){color.END()}: "
                )
                t += 1
                if t >= 8:
                    print("\nYou have tried to enter a username too many times.\n")
                    print(
                        "You will be playing on 'Guest' mode. Your score will not be saved."
                    )
                    user = "guest"
                    score = 0
                    break
        if user != "guest":
            cursor.execute(
                f"INSERT INTO users (name, score) VALUES (?, 0)", (target_user,)
            )
            print(f"\nWelcome {target_user}!\n")
            print("You recieved 5 points for signing up!")
            user = target_user
            score = 5
    else:
        print(
            "\nWelcome! You will be playing on 'Guest' mode. Your score will not be recorded.\n"
        )
        user = "guest"
        score = 0
elif newUser[0] == "n":
    singin = input("Would you like to log in? (y/n): ").lower()
    if singin[0] == "y":
        target_user = input("Please enter your username: ").strip()
        allUsers = cursor.execute("SELECT name FROM users").fetchall()

        for username in allUsers:
            if username[0] == target_user:
                user = username[0]
                tempscore = cursor.execute(
                    "SELECT score FROM users WHERE name = ?",
                    (user,),
                ).fetchall()
                score = tempscore[0][0]
                print(f"\nWelcome back {user}!")
                print(f"Your current score is: {score}\n")
            else:
                t += 1
                if t >= len(allUsers):
                    print(f"{color.RED()}That username does not exist.{color.END()}")
                    print(
                        "You will be playing on 'Guest' mode. Your score will not be saved.\n"
                    )
                    user = "guest"
                    score = 0

            # while target_user not in allUsers:
            #     print(f"\n{color.RED()}Error:{color.END()} Username not found.")
            #     target_user = input("Please enter your username: ")
            #     if t >= 8:
            #         print("\nYou have tried to enter a username too many times.\n")
            #         print(
            #             "You will be playing on 'Guest' mode. Your score will not be saved."
            #         )
            #         user = "guest"
            #         e = True
            #         break

            # if e == True:
            #     score = 0
            # else:
            #     user = target_user[3 : len(target_user) - 4]
            #     tempscore = cursor.execute(
            #         "SELECT score FROM users WHERE name = ?",
            #         (user,),
            #     ).fetchall()
            #     score = tempscore[0][0]
            #     print(f"\nWelcome {user}!")
            #     print(f"Your current score is: {score}\n")
    else:
        print(
            "\nWelcome! You will be playing on 'Guest' mode. Your score will not be recorded.\n"
        )
        user = "guest"
else:
    print(
        "\nYou did not enter a valid response. You will be playing on 'Guest' mode. Your score will not be recorded.\n"
    )
    user = "guest"

difficultyFunc()
for letter in secretWord:
    hint.append("_")
print("-" * 50)
print(f"\nYour hint is: " + " ".join(hint) + "\n")

# Run the game.
while playagain == "y":
    while guess != secretWord:
        # Check number of guesses left and play again.
        if guess_count <= 0:
            print(f"You ran out of guesses! The word was {secretWord}! You lost.")
            score = score + newPoints
            print(f"Points earned: {newPoints}  |  Total Score: {score}")
            if difficulty == "cheater":
                cursor.execute(
                    "UPDATE users SET score = ? WHERE name = ?", (score, user)
                )
                connection.commit()
                with closing(sqlite3.connect("users.db")) as connection:
                    with closing(connection.cursor()) as cursor:
                        rows = cursor.execute("SELECT 1").fetchall()
                        print("Game saved!")
                quit()
            playagain = input("Would you like to play again? (y/n): ").lower()
            if playagain == "y":
                reset()
            else:
                print("\nThanks for playing!")
                if difficulty != "guest":
                    print(f"See you again soon {user}!")
                    cursor.execute(
                        "UPDATE users SET score = ? WHERE name = ?", (score, user)
                    )
                    connection.commit()
                    with closing(sqlite3.connect("users.db")) as connection:
                        with closing(connection.cursor()) as cursor:
                            rows = cursor.execute("SELECT 1").fetchall()
                            print("Game saved!")
                    quit()
                else:
                    print(f"'Guest' Score : {score}")
                    guestfinal = input(
                        "\nYou have been playing on 'Guest' mode. Would you liked to create a \
                Username so that your score will be saved(y/n)? "
                    )
                    if guestfinal[0] == "y":
                        target_user = input(
                            f"Please enter your username(Make it unique): "
                        )
                        while target_user in allUsers:
                            print(
                                f"\nThat username is already taken. Please try again."
                            )
                            target_user = input(
                                f"Please enter your username{color.UNDERLINE}(Make it unique){color.END()}: "
                            )
                            t += 1
                            if t >= 8:
                                print(
                                    "\nYou have tried to enter a username too many times. Your score was not saved.\n"
                                )
                                user = "guest"
                                break
                        if user != "guest":
                            cursor.execute(
                                f"INSERT INTO users (name, score) VALUES (?, ?)",
                                (
                                    target_user,
                                    score,
                                ),
                            )
                        else:
                            print("Consider singing up next time!")
                            quit()
                    else:
                        print("Consider singing up next time!")
                        quit()
        # Main game loop.
        else:
            print(f"Guesses left: {guess_count}")
            guess = input("Guess a word: ")
            guess = guess.lower()
            guess_count -= 1
            hintUpdated = []
            # Reset hint
            for letter in secretWord:
                hintUpdated.append("_")
            # Check if user guessed correct word and play again.
            if guess == secretWord:
                print(
                    f"You guessed correctly! The word was {secretWord}! You had {guess_count} guesses left!"
                )
                if difficulty != "easy":
                    newPoints = baseNewPoints * (guess_count * multiplyer)
                elif difficulty == "easy":
                    newPoints = baseNewPoints
                if difficulty == "cheater":
                    score = score + newPoints
                    if user != "guest":
                        cursor.execute(
                            "UPDATE users SET score = ? WHERE name = ?", (score, user)
                        )
                        connection.commit()
                        with closing(sqlite3.connect("users.db")) as connection:
                            with closing(connection.cursor()) as cursor:
                                rows = cursor.execute("SELECT 1").fetchall()
                                print("Game saved!")
                    quit()
                # playagain = input("Would you like to play again? (y/n): ").lower()
                # if playagain == "y":
                #     score = score + newPoints
                #     reset()
                # else:
                #     score = score + newPoints
                print(
                    f"Points earned: {newPoints}  |  Total Score: {score + newPoints}"
                )
                playagain = input("Would you like to play again? (y/n): ").lower()
                if playagain[0] == "y":
                    score = score + newPoints
                    reset()
                else:
                    if user != "guest":
                        print("Thanks for playing! See you again soon!")
                        score = score + newPoints
                        cursor.execute(
                            "UPDATE users SET score = ? WHERE name = ?", (score, user)
                        )
                        connection.commit()
                        with closing(sqlite3.connect("users.db")) as connection:
                            with closing(connection.cursor()) as cursor:
                                rows = cursor.execute("SELECT 1").fetchall()
                                print("Game saved!")
                        quit()
                    else:
                        print(f"'Guest' Score : {score}")
                        guestfinal = input(
                            "You have been playing on 'Guest' mode. Would you liked to create a \
                    Username so that your score will be saved(y/n)? "
                        )
                        if guestfinal[0] == "y":
                            target_user = input(
                                f"Please enter your username(Make it unique): "
                            )
                            if target_user in allUsers:
                                while target_user in allUsers:
                                    print(
                                        f"\nThat username is already taken. Please try again."
                                    )
                                    target_user = input(
                                        f"Please enter your username{color.UNDERLINE}(Make it unique){color.END()}: "
                                    )
                                    t += 1
                                    if t >= 8:
                                        print(
                                            "\nYou have tried to enter a username too many times. Your score was not saved.\n"
                                        )
                                        user = "guest"
                                        break
                            if user != "guest":
                                print(f"Thanks for signing up {user}!")
                                cursor.execute(
                                    f"INSERT INTO users (name, score) VALUES (?, ?)",
                                    (
                                        target_user,
                                        score,
                                    ),
                                )
                                print("Game saved!")
                                quit()

                            else:
                                print("Consider singing up next time!")
                                quit()
                        else:
                            print("Consider singing up next time!")
                            quit()

                # Check if user gave up on current word and play again.
            elif guess == "giveup":
                score = score + newPoints
                print(f"The word was {secretWord}! You lost.")
                if difficulty == "cheater":
                    print(f"{color.RED()}Quitter!{color.END()}")
                    quit()
                playagain = input("Would you like to play again? (y/n): ").lower()
                if playagain == "y":
                    reset()
                else:
                    print("Thanks for playing! See you again soon!")
                    if user != "guest":
                        cursor.execute(
                            "UPDATE users SET score = ? WHERE name = ?", (score, user)
                        )
                        connection.commit()
                        with closing(sqlite3.connect("users.db")) as connection:
                            with closing(connection.cursor()) as cursor:
                                rows = cursor.execute("SELECT 1").fetchall()
                                print("Game saved!")
                    quit()
            # Check if user wants a hint.
            elif guess == "hint":
                hintLetter = ""
                a = 0
                # Easy difficulty hint.
                if difficulty == "easy":
                    hintLetter = random.choice(secretWord)
                    while hintLetter in correct and len(correct) <= len(secretWord):
                        hintLetter = random.choice(secretWord)
                        a += 1
                        if a >= 30:
                            print(
                                "No more hints available! (There are multiples of some letters!)"
                            )
                            break
                    print(f"\nYour hint is: " + " ".join(hintLetter) + "\n")
                    guess_count += 1
                # Medium difficulty hint.
                elif difficulty == "medium" and score > 2:
                    hintLetter = random.choice(secretWord)
                    while hintLetter in correct and len(correct) < len(secretWord):
                        hintLetter = random.choice(secretWord)
                        a += 1
                        if a >= 30:
                            print(
                                "No more hints available! (There are multiples of some letters!)"
                            )
                            break
                    print(
                        f"\nYour hint is: "
                        + " ".join(hintLetter)
                        + "\nThat cost 1 guess!\n"
                    )
                    score = score - 2
                # Hard difficulty hint.
                elif difficulty == "hard":
                    print(f"Hard mode has no hints!")
                # Cheater hint
                elif difficulty == "cheater":
                    print(f"You think we would give you a hint? HA!\n")
                    print(
                        f"{color.RED()}{color.BOLD()}C\nH\nE\nA\nT\nE\nR\n!{color.END()}"
                    )
                    quit()
                else:
                    print("You do not have enough points to get a hint!")
                    guess_count += 1
            elif len(guess) >= len(secretWord) + 7:
                print("Trying to cheat? No more multiplier for you!")
                multiplyer = 0
            elif guess == "aeiou":
                print("Trying to cheat? -5 points!")
                score = score - 5
            # Check guess letters declaring variable 'i' and updating hint.
            else:
                for letter in guess:
                    if i < letterCount:
                        if letter in secretWord:
                            if letter == secretWord[i]:
                                hintUpdated[i] = letter.upper()
                                checkCorrectList(letter)
                                i += 1
                            else:
                                hintUpdated[i] = letter.lower()
                                checkCorrectList(letter)
                                i += 1
                        else:
                            hintUpdated[i] = "_"
                            i += 1
                    else:
                        checkCorrectList(letter)
                        hintUpdated.append(letter.lower())
                i = 0
                # Displays all corect letters guessed
                if difficulty == "easy" or difficulty == "medium":
                    print(
                        f"\nLetters you guessed that are in the answer: "
                        + " ".join(correct)
                    )
                # Prints new hint
                print(f"\nYour hint is: " + " ".join(hintUpdated) + "\n")
