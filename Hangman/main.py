# Updated 10 April 2024
# Originally written during a boring cs lecture
# Enjoy

import random
import os

class Game:
    def __init__(self):
        self._restart()
        self.__make_stages__()
        self.letters = "abcdefghijklmnopqrstuvwxyz"

    def _restart(self) -> None:
        with open("words.txt", "r") as f:
            data = f.read()
            words = data.split("\n")
        self.word = random.choice(words)
        self.guessed = set()
        self.stage = 0

    def __make_stages__(self) -> None:
        self.stages = ["\n\n\n\n\n",
            "\n\n\n\n\n_______________",
            "\n       |\n       |\n       |\n       |\n_______|_______",
            "       _____\n       |\n       |\n       |\n       |\n_______|_______",
            "       _____\n       |   |\n       |\n       |\n       |\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |\n       |\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |   |\n       |\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |  -|\n       |\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |  -|-\n       |\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |  -|-\n       |  /\n_______|_______",
            "       _____\n       |   |\n       |   O\n       |  -|-\n       |  / \\\n_______|_______"]

    def _guess(self, letter: str) -> None:
        if self._isLost() or self._isWon():
            return

        if len(letter) > 1:
            if letter == self.word:
                for l in self.word:
                    self.guessed.add(l)
                self._endGame()

        if letter not in self.word and letter not in self.guessed:
            self.stage += 1
        self.guessed.add(letter)

    def _print(self) -> None:
        if self.stage > 10:
            self.stage = 10
        word = []
        for l in self.word:
            if l in self.guessed:
                word.append(l)
            else:
                if len(word) > 0 and word[-1] == "_":
                    word.append(" ")
                word.append("_")
        print(self.stages[self.stage])
        print("\nWord:", "".join(word))
        print("\nGuessed: " + ", ".join(self.guessed))
        print("\nRemaining: " + ", ".join([l for l in self.letters if l not in self.guessed]) + "\n")

    def _isWon(self) -> bool:
        for l in self.word:
            if l not in self.guessed:
                return False
        return True

    def _isLost(self) -> bool:
        return self.stage >= 10
    
    def play(self) -> None:
        while True:
            os.system("cls")
            self._print()
            letter = input("Guess: ").strip()
            if len(letter) < 1:
                continue
            self._guess(letter)
            if self._isWon() or self._isLost():
                self._endGame()
                break
                
    def _endGame(self) -> None:
        os.system("cls")
        self._print()
        if self._isWon():
            print("YOU WON!")
        else:
            print("The word was " + self.word)
            print("Read a dictionary you idiot")
            
    def loopPlay(self) -> None:
        self.play()
        while True:
            answer = input("\nPlay again? ")
            if len(answer) > 0:
                break
            self._restart()
            self.play()

if __name__ == "__main__":
    g = Game()
    g.loopPlay()