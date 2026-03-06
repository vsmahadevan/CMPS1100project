import pytest
import tkinter as tk
import sliding_puzzle_project

EMPTY = 0

# -------------------- Fixture --------------------
@pytest.fixture
def app():
    root = tk.Tk()
    root.withdraw()  # hide GUI

    puzzle = sliding_puzzle_project.SlidingPuzzleApp(root, size=3)
    puzzle.game_over = False  # allow clicks during tests

    yield puzzle
    root.destroy()


# -------------------- Helper --------------------
def swap_last_two_tiles(board):
    """Helper to swap last two tiles (used for move tests)."""
    board[-1], board[-2] = board[-2], board[-1]


# -------------------- Tests --------------------
def test_reset_creates_solvable_board(app):
    """Check that restarting game produces a solvable board with correct tiles."""
    app.restart_game()
    # Board should contain same tiles as goal_tiles
    assert sorted(app.board) == sorted(app.goal_tiles)
    # Board must be solvable
    assert app.is_solvable(app.board) is True


def test_is_adjacent_true(app):
    size = app.size
    assert app.is_adjacent(0, 1) is True
    assert app.is_adjacent(0, size) is True


def test_is_adjacent_false(app):
    size = app.size
    assert app.is_adjacent(0, size + 1) is False
    assert app.is_adjacent(0, size * size - 1) is False


def test_swap_logic(app):
    board = app.goal_tiles[:]
    swap_last_two_tiles(board)
    assert board[-1] != app.goal_tiles[-1]
    assert board[-2] != app.goal_tiles[-2]


def test_is_solved_false_when_moved(app):
    board = app.goal_tiles[:]
    swap_last_two_tiles(board)
    app.board = board
    assert app.board != app.goal_tiles


def test_on_click_valid_move(app):
    board = app.goal_tiles[:]
    swap_last_two_tiles(board)
    app.board = board

    class Event:
        x = (app.size - 1) * app.tile_px
        y = (app.size - 1) * app.tile_px

    app.on_click(Event())
    # After click, board should match goal_tiles
    assert app.board == app.goal_tiles


def test_on_click_invalid_move(app):
    board = app.goal_tiles[:]
    swap_last_two_tiles(board)
    app.board = board

    class Event:
        x = 0
        y = 0  # click far away, not adjacent

    old_board = app.board[:]
    app.on_click(Event())
    assert app.board == old_board


def test_shuffle_changes_board(app):
    original = app.goal_tiles[:]
    app.shuffle_board()
    assert app.board != original


def test_set_size_changes_board_dimensions(app):
    app.change_size(4)
    assert app.size == 4
    assert app.board is not None
    assert len(app.board) == 16


def test_shuffle_creates_solvable_board(app):
    app.shuffle_board()
    assert app.is_solvable(app.board) is True


if __name__ == "__main__":
    pytest.main()def test_reset_creates_solved_board(app):
    app.reset()
    expected = [[1,2,3],[4,5,6],[7,8,0]]
    assert app.board == expected


def test_is_adjacent_true(app):
    assert app.is_adjacent((2,2), (2,1)) is True
    assert app.is_adjacent((1,1), (0,1)) is True


def test_is_adjacent_false(app):
    assert app.is_adjacent((0,0), (2,2)) is False
    assert app.is_adjacent((1,0), (0,2)) is False


def test_swap_changes_positions(app):
    app.board = [[1,2,3],[4,5,6],[7,8,0]]
    app.swap((2,2), (2,1))
    assert app.board[2][2] == 8
    assert app.board[2][1] == 0


def test_is_solved_false_when_moved(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    assert app.is_solved() is False


def test_on_click_valid_move(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    app.on_click((2,2))  # swap with blank
    assert app.board[2][2] == 0
    assert app.board[2][1] == 8


def test_on_click_invalid_move(app):
    app.board = [[1,2,3],[4,5,6],[7,0,8]]
    old_board = [row[:] for row in app.board]
    app.on_click((0,0))  # invalid move
    assert app.board == old_board  # board unchanged


def test_shuffle_changes_board(app):
    original = [row[:] for row in app.board]
    app.shuffle()
    assert app.board != original  # after shuffle, board should change


def test_set_size_changes_board_dimensions(app):
    app.set_size(4)
    assert len(app.board) == 4
    assert len(app.board[0]) == 4

def is_solvable(self, board):
    flat = [num for row in board for num in row if num != 0]
    inversions = 0

    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1

    # For odd grid size (3x3)
    if self.size % 2 == 1:
        return inversions % 2 == 0

    # For even grid size
    blank_row = next(i for i, row in enumerate(board) if 0 in row)
    blank_row_from_bottom = self.size - blank_row

    if blank_row_from_bottom % 2 == 0:
        return inversions % 2 == 1
    else:
        return inversions % 2 == 0
    
def test_shuffle_creates_solvable_board(app):
    app.shuffle()
    assert app.is_solvable(app.board) is True

if __name__ == "__main__":
    pytest.main()
