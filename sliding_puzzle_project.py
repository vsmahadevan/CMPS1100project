import tkinter as tk
import random
import time
from PIL import Image, ImageTk

EMPTY = 0
IMAGE_PATH = "puppy.jpg"   # Keep your image in the same folder


class SlidingPuzzleApp:
    def __init__(self, root, size=3, tile_px=120):
        self.root = root
        self.size = size
        self.tile_px = tile_px
        self.board_px = self.size * self.tile_px

        self.root.title("Sliding Puzzle")
        self.root.resizable(False, False)
        self.root.configure(bg="#f7f4ef")

        self.moves = 0
        self.start_time = None
        self.timer_running = False
        self.game_over = False
        self.confetti = []
        self.tile_images = {}
        self.goal_tiles = []
        self.source_image = None

        # Load original image once
        self.original_image = Image.open(IMAGE_PATH)

        # ---------- Title ----------
        title = tk.Label(
            root,
            text="🧩 Sliding Puzzle Challenge 🧩",
            font=("Helvetica", 26, "bold"),
            fg="#2c3e50",
            bg="#f7f4ef"
        )
        title.pack(pady=(12, 6))

        # ---------- Controls ----------
        controls = tk.Frame(root, bg="#f7f4ef")
        controls.pack(pady=(0, 8))

        self.status = tk.Label(
            controls,
            text="Click tiles next to the empty space, including wrap-around edge moves.",
            font=("Helvetica", 12, "bold"),
            fg="#34495e",
            bg="#f7f4ef"
        )
        self.status.grid(row=0, column=0, columnspan=3, pady=(0, 8))

        self.moves_label = tk.Label(
            controls,
            text="Moves: 0",
            font=("Helvetica", 12, "bold"),
            fg="#34495e",
            bg="#f7f4ef"
        )
        self.moves_label.grid(row=1, column=0, padx=12)

        self.timer_label = tk.Label(
            controls,
            text="Time: 0s",
            font=("Helvetica", 12, "bold"),
            fg="#34495e",
            bg="#f7f4ef"
        )
        self.timer_label.grid(row=1, column=1, padx=12)

        play_again_btn = tk.Button(
            controls,
            text="🔄 Play Again",
            font=("Helvetica", 11, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            activeforeground="white",
            relief="flat",
            padx=10,
            pady=5,
            command=self.restart_game
        )
        play_again_btn.grid(row=1, column=2, padx=12)

        # ---------- Size selector ----------
        size_frame = tk.Frame(root, bg="#f7f4ef")
        size_frame.pack(pady=(0, 10))

        tk.Label(
            size_frame,
            text="Puzzle Size:",
            font=("Helvetica", 11, "bold"),
            fg="#34495e",
            bg="#f7f4ef"
        ).pack(side="left", padx=5)

        tk.Button(
            size_frame,
            text="3x3",
            font=("Helvetica", 10, "bold"),
            bg="#ecf0f1",
            relief="flat",
            padx=8,
            pady=4,
            command=lambda: self.change_size(3)
        ).pack(side="left", padx=4)

        tk.Button(
            size_frame,
            text="4x4",
            font=("Helvetica", 10, "bold"),
            bg="#ecf0f1",
            relief="flat",
            padx=8,
            pady=4,
            command=lambda: self.change_size(4)
        ).pack(side="left", padx=4)

        tk.Button(
            size_frame,
            text="5x5",
            font=("Helvetica", 10, "bold"),
            bg="#ecf0f1",
            relief="flat",
            padx=8,
            pady=4,
            command=lambda: self.change_size(5)
        ).pack(side="left", padx=4)

        # ---------- Main layout ----------
        main_frame = tk.Frame(root, bg="#f7f4ef")
        main_frame.pack(padx=12, pady=(0, 12))

        self.canvas = tk.Canvas(
            main_frame,
            width=self.board_px,
            height=self.board_px,
            highlightthickness=0,
            bd=0,
            bg="white"
        )
        self.canvas.grid(row=0, column=0, padx=(0, 16))

        preview_panel = tk.Frame(main_frame, bg="#f7f4ef")
        preview_panel.grid(row=0, column=1, sticky="n")

        preview_title = tk.Label(
            preview_panel,
            text="Goal Image",
            font=("Helvetica", 13, "bold"),
            fg="#2c3e50",
            bg="#f7f4ef"
        )
        preview_title.pack(pady=(0, 8))

        self.preview_display = tk.Label(
            preview_panel,
            bd=2,
            relief="solid",
            bg="white"
        )
        self.preview_display.pack()

        preview_hint = tk.Label(
            preview_panel,
            text="Rebuild the image!",
            font=("Helvetica", 10),
            fg="#5d6d7e",
            bg="#f7f4ef"
        )
        preview_hint.pack(pady=(8, 0))

        self.canvas.bind("<Button-1>", self.on_click)

        self.load_and_slice_image()
        self.restart_game()

    def get_square_cropped_image(self, img):
        """Crop image to a square without stretching."""
        width, height = img.size
        side = min(width, height)

        left = (width - side) // 2
        top = (height - side) // 2
        right = left + side
        bottom = top + side

        return img.crop((left, top, right, bottom))

    def load_and_slice_image(self):
        """Load image, crop to square, make preview, and slice into tiles."""
        self.tile_images = {}
        self.goal_tiles = []

        img = self.original_image.copy()
        img = self.get_square_cropped_image(img)
        img = img.resize((self.board_px, self.board_px), Image.Resampling.LANCZOS)
        self.source_image = img

        # Preview image
        preview_size = 140
        preview = img.resize((preview_size, preview_size), Image.Resampling.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(preview)
        self.preview_display.config(image=self.preview_photo)

        tile_number = 1

        for row in range(self.size):
            for col in range(self.size):
                if row == self.size - 1 and col == self.size - 1:
                    self.goal_tiles.append(EMPTY)
                    continue

                left = col * self.tile_px
                top = row * self.tile_px
                right = left + self.tile_px
                bottom = top + self.tile_px

                tile_img = img.crop((left, top, right, bottom))
                photo = ImageTk.PhotoImage(tile_img)

                self.goal_tiles.append(tile_number)
                self.tile_images[tile_number] = photo
                tile_number += 1

    def restart_game(self):
        """Reset counters and reshuffle the board."""
        self.shuffle_board()

        self.moves = 0
        self.moves_label.config(text="Moves: 0")

        self.start_time = time.time()
        self.timer_running = True
        self.game_over = False
        self.confetti = []

        self.status.config(
            text="Click tiles next to the empty space, including wrap-around edge moves."
        )
        self.draw_board()
        self.update_timer()

    def change_size(self, new_size):
        """Switch between 3x3, 4x4, and 5x5."""
        self.size = new_size
        self.board_px = self.size * self.tile_px
        self.canvas.config(width=self.board_px, height=self.board_px)

        self.load_and_slice_image()
        self.restart_game()

    def shuffle_board(self, steps=300):
        """
        Shuffle by making legal moves from the solved board.
        This guarantees the board is reachable under wrap-around rules.
        """
        self.board = self.goal_tiles[:]
        empty_index = self.board.index(EMPTY)
        last_move = None

        for _ in range(steps):
            possible_moves = []

            for i in range(len(self.board)):
                if i != empty_index and self.is_adjacent(i, empty_index):
                    if i != last_move:
                        possible_moves.append(i)

            if not possible_moves:
                for i in range(len(self.board)):
                    if i != empty_index and self.is_adjacent(i, empty_index):
                        possible_moves.append(i)

            move_index = random.choice(possible_moves)
            self.board[empty_index], self.board[move_index] = (
                self.board[move_index],
                self.board[empty_index],
            )
            last_move = empty_index
            empty_index = move_index

        if self.board == self.goal_tiles:
            self.shuffle_board(steps)

    def count_inversions(self, board):
        arr = [x for x in board if x != EMPTY]
        inversions = 0

        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                if arr[i] > arr[j]:
                    inversions += 1

        return inversions

    def is_solvable(self, board):
        """
        Kept from original version, but no longer used for shuffling
        now that wrap-around moves are allowed.
        """
        inversions = self.count_inversions(board)

        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            empty_index = board.index(EMPTY)
            empty_row_from_top = empty_index // self.size
            empty_row_from_bottom = self.size - empty_row_from_top

            if empty_row_from_bottom % 2 == 0:
                return inversions % 2 == 1
            else:
                return inversions % 2 == 0

    def draw_board(self):
        self.canvas.delete("all")

        for index, value in enumerate(self.board):
            row = index // self.size
            col = index % self.size
            x = col * self.tile_px
            y = row * self.tile_px

            if value == EMPTY:
                self.canvas.create_rectangle(
                    x, y, x + self.tile_px, y + self.tile_px,
                    fill="white",
                    outline="white"
                )
            else:
                self.canvas.create_image(
                    x, y,
                    image=self.tile_images[value],
                    anchor="nw"
                )

    def on_click(self, event):
        if self.game_over:
            return

        col = event.x // self.tile_px
        row = event.y // self.tile_px

        if not (0 <= row < self.size and 0 <= col < self.size):
            return

        clicked_index = row * self.size + col
        empty_index = self.board.index(EMPTY)

        if self.is_adjacent(clicked_index, empty_index):
            self.board[empty_index], self.board[clicked_index] = (
                self.board[clicked_index],
                self.board[empty_index],
            )

            self.moves += 1
            self.moves_label.config(text=f"Moves: {self.moves}")
            self.draw_board()

            if self.board == self.goal_tiles:
                self.handle_win()

    def is_adjacent(self, i, j):
        row1, col1 = divmod(i, self.size)   # clicked tile
        row2, col2 = divmod(j, self.size)   # empty tile

        # Normal adjacent move
        if abs(row1 - row2) + abs(col1 - col2) == 1:
            return True

        # Wrap-around move in same column: top <-> bottom
        if col1 == col2 and abs(row1 - row2) == self.size - 1:
            return True

        # Wrap-around move in same row: left <-> right
        if row1 == row2 and abs(col1 - col2) == self.size - 1:
            return True

        return False

    def update_timer(self):
        if self.timer_running and not self.game_over:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}s")
            self.root.after(1000, self.update_timer)

    def handle_win(self):
        self.game_over = True
        self.timer_running = False
        elapsed = int(time.time() - self.start_time)

        self.status.config(
            text=f"🎉 YOU WIN!!! 🎉 Solved in {self.moves} moves and {elapsed} seconds!"
        )
        self.celebrate_win()

    def celebrate_win(self):
        colors = [
            "red", "orange", "yellow", "green",
            "blue", "purple", "pink", "cyan", "gold"
        ]
        self.confetti = []

        for _ in range(160):
            x = random.randint(0, self.board_px)
            y = random.randint(-250, -10)
            w = random.randint(4, 10)
            h = random.randint(6, 12)

            if random.choice([True, False]):
                piece = self.canvas.create_rectangle(
                    x, y, x + w, y + h,
                    fill=random.choice(colors),
                    outline=""
                )
            else:
                piece = self.canvas.create_oval(
                    x, y, x + w, y + h,
                    fill=random.choice(colors),
                    outline=""
                )

            dx = random.randint(-3, 3)
            dy = random.randint(3, 8)
            self.confetti.append((piece, dx, dy))

        self.animate_confetti()

    def animate_confetti(self):
        still_falling = False
        new_confetti = []

        for piece, dx, dy in self.confetti:
            self.canvas.move(piece, dx, dy)
            coords = self.canvas.coords(piece)

            if coords and coords[1] < self.board_px + 30:
                still_falling = True
                new_confetti.append((piece, dx, dy))

        self.confetti = new_confetti

        if still_falling:
            self.root.after(30, self.animate_confetti)


if __name__ == "__main__":
    root = tk.Tk()
    app = SlidingPuzzleApp(root, size=3, tile_px=120)
    root.mainloop()
