import tkinter as tk
import random
import time

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
SNAKE_SPEED = 150  # in milliseconds

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # Initialize the snake with one segment and place the food
        self.snake = [(100, 100)]
        self.food = self.create_food()
        self.direction = "Right"

        # Bind the arrow keys to the change_direction function
        self.root.bind("<Key>", self.change_direction)

        # Initialize game state
        self.game_over = False
        self.score = 0

        # Create a "Restart" button
        self.restart_button = tk.Button(root, text="Restart", command=self.restart_game)
        self.restart_button.pack()

        # Start the game loop
        self.update()

    def create_food(self):
        # Create and return the coordinates for a new food item
        x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        return (x, y)

    def draw_snake(self):
        # Draw the snake on the canvas
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + GRID_SIZE, y + GRID_SIZE, fill="green"
            )

    def draw_food(self):
        # Draw the food on the canvas
        x, y = self.food
        self.canvas.create_oval(
            x, y, x + GRID_SIZE, y + GRID_SIZE, fill="red"
        )

    def change_direction(self, event):
        # Change the snake's direction based on arrow key presses
        if event.keysym == "Up" and self.direction != "Down":
            self.direction = "Up"
        elif event.keysym == "Down" and self.direction != "Up":
            self.direction = "Down"
        elif event.keysym == "Left" and self.direction != "Right":
            self.direction = "Left"
        elif event.keysym == "Right" and self.direction != "Left":
            self.direction = "Right"

    def check_collision(self):
        # Check if the snake collides with the wall or itself
        x, y = self.snake[0]
        if (
            x < 0
            or x >= WIDTH
            or y < 0
            or y >= HEIGHT
            or self.snake[0] in self.snake[1:]
        ):
            return True
        return False

    def move_snake(self):
        # Move the snake based on its current direction
        x, y = self.snake[0]
        if self.direction == "Up":
            y -= GRID_SIZE
        elif self.direction == "Down":
            y += GRID_SIZE
        elif self.direction == "Left":
            x -= GRID_SIZE
        elif self.direction == "Right":
            x += GRID_SIZE

        self.snake.insert(0, (x, y))

        # Check if the snake ate the food and update the score
        if self.snake[0] == self.food:
            self.score += 1
            self.food = self.create_food()
        else:
            self.snake.pop()

    def restart_game(self):
        # Reset the game state for a new game
        self.snake = [(100, 100)]
        self.food = self.create_food()
        self.direction = "Right"
        self.game_over = False
        self.score = 0
        self.update()

    def update(self):
        # Main game loop
        if not self.game_over:
            self.canvas.delete("all")
            self.move_snake()
            self.draw_snake()
            self.draw_food()

            if self.check_collision():
                # End the game if a collision occurs
                self.game_over = True
                self.canvas.create_text(
                    WIDTH // 2,
                    HEIGHT // 2,
                    text="Game Over! Score: " + str(self.score),
                    fill="red",
                    font=("Helvetica", 20),
                )
            else:
                # Continue the game loop by scheduling the next update
                self.root.after(SNAKE_SPEED, self.update)
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
