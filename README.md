# Sliding Puzzle Project

## Description

This project implements a sliding puzzle game using Python and Tkinter.
This project is a sliding puzzle game that utilizes Python as well as Tinter. It displays an image divided into tiles that is arranged on a grid. One of the tile spaces is empty so that players can slide these tiles into the empty space. The objective of the game is to rearrange these tiles to return the image back to the original order.

This repository also contains a test suite to ensure that the puzzle works as intended.

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
* Tkinter (usually included with Python) version 8.6
* Pillow (for image handling) version 12.1.1
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

The tests check:

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
