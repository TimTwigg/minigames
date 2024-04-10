import argparse

from Hangman.Hangman import Hangman
from Minesweeper.Minesweeper import Minesweeper

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play Hangman or Minesweeper")
    parser.add_argument("game", help="Game to play", choices=["hangman", "minesweeper"])
    args = parser.parse_args()
    
    if args.game == "hangman":
        g = Hangman()
    elif args.game == "minesweeper":
        g = Minesweeper()
    else:
        raise ValueError("Invalid game")
    g.play()