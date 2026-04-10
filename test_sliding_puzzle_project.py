import sys
sys.path.append("/Users/vedikamahadevan/CMPS1100 Practice")

import pytest
import tkinter as tk
import sliding_puzzle_project


# ---------------- FIXTURE ----------------
@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()

    puzzle = sliding_puzzle_project.SlidingPuzzleApp(root, size=3, tile_px=120)

    yield puzzle

    root.destroy()


# ---------------- TESTS ----------------

def test_restart_creates_valid_board(app):
    app.restart_game()
    assert len(app.board) == len(app.goal_tiles)
    assert sorted(app.board) == sorted(app.goal_tiles)


def test_shuffle_changes_board(app):
    original = app.goal_tiles[:]
    app.shuffle_board()
    assert app.board != original


def test_shuffle_creates_solvable_board(app):
    app.shuffle_board()
    assert app.is_solvable(app.board) is True


def test_change_size_updates_board(app):
    app.change_size(4)
    assert app.size == 4
    assert len(app.board) == 16


def test_is_adjacent_true(app):
    assert app.is_adjacent(0, 1) is True
    assert app.is_adjacent(0, 3) is True


def test_is_adjacent_false(app):
    assert app.is_adjacent(0, 4) is False
    assert app.is_adjacent(0, 8) is False


def test_on_click_valid_move(app):
    app.restart_game()

    empty = app.board.index(0)

    # pick a safe neighbor if possible
    if empty > 0:
        target = empty - 1
    else:
        target = empty + 1

    class Event:
        x = (target % app.size) * app.tile_px
        y = (target // app.size) * app.tile_px

    old = app.board[:]
    app.on_click(Event())

    assert app.board != old


def test_on_click_invalid_move(app):
    app.restart_game()

    empty = app.board.index(0)

    # find a tile that is GUARANTEED NOT adjacent
    invalid = None
    for i in range(len(app.board)):
        if not app.is_adjacent(i, empty):
            invalid = i
            break

    class Event:
        x = (invalid % app.size) * app.tile_px
        y = (invalid // app.size) * app.tile_px

    old = app.board[:]
    app.on_click(Event())

    assert app.board == old


# ---------------- RUN SUPPORT (IMPORTANT) ----------------
if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main(["-v", __file__]))
