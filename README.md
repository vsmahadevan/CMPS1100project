# Sliding Puzzle Project

## Description

This project implements a sliding puzzle game using Python and Tkinter.
The puzzle displays an image that is divided into tiles arranged in a grid. One tile space is empty, allowing the player to slide neighboring tiles into the empty space. The goal of the game is to rearrange the tiles so the image returns to its original solved order.

The program also includes automated tests written with Pytest to verify that the puzzle logic works correctly.

## Features

* Graphical puzzle board created with Tkinter
* Click tiles to slide them into the empty space
* Shuffle function to randomize the puzzle
* Solvable puzzle generation
* Multiple board sizes supported
* Automated unit tests for puzzle logic

## Requirements

You must have the following installed:

* Python 3
* Tkinter (usually included with Python)
* Pillow (for image handling)
* Pytest (for running tests)

Install required packages with:

pip install pillow pytest

## How to Run the Game

Run the main puzzle application with:

python sliding_puzzle_project.py

This will open the puzzle window where you can play the game by clicking tiles adjacent to the blank space.

## How to Run the Tests

To run the automated tests, open a terminal in the project folder and run:

pytest

You can also run the test file directly with:

python test_sliding_puzzle_project.py

The tests check important puzzle behaviors including:

* Board reset
* Valid and invalid tile moves
* Tile swapping
* Puzzle solved state
* Shuffle behavior
* Puzzle solvability

## Project Files

* sliding_puzzle_project.py – main sliding puzzle game implementation
* test_sliding_puzzle_project.py – automated tests for puzzle logic
* README.md – instructions and project description

## Author

Sarah Blufstein, Ellie Loftin, Vedika Mahadevan
