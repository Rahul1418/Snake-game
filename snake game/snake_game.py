import tkinter as tk
import random

# Constants for game configuration
ROWS, COLS, TILE_SIZE = 25, 25, 25
WINDOW_WIDTH, WINDOW_HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Set up the game window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

canvas = tk.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()

# Center the window on the screen
window.update_idletasks()
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(window.winfo_screenwidth() - WINDOW_WIDTH) // 2}+{(window.winfo_screenheight() - WINDOW_HEIGHT) // 2}")

# Initialize game variables
head = Segment(TILE_SIZE * 5, TILE_SIZE * 5)  # Snake's initial position
food = Segment(TILE_SIZE * 10, TILE_SIZE * 10)
direction_x, direction_y = 0, 0
snake_body = []
game_over = False
score = 0

def handle_key(event):
    """Change the direction of the snake based on key press."""
    global direction_x, direction_y, game_over

    if game_over:
        return  # Modify here to reset game variables to restart

    if event.keysym == "Up" and direction_y != 1:
        direction_x, direction_y = 0, -1
    elif event.keysym == "Down" and direction_y != -1:
        direction_x, direction_y = 0, 1
    elif event.keysym == "Left" and direction_x != 1:
        direction_x, direction_y = -1, 0
    elif event.keysym == "Right" and direction_x != -1:
        direction_x, direction_y = 1, 0

def update_game():
    """Update the game state."""
    global head, food, snake_body, game_over, score

    if game_over:
        return

    # Check for collisions with walls
    if head.x < 0 or head.x >= WINDOW_WIDTH or head.y < 0 or head.y >= WINDOW_HEIGHT:
        game_over = True
        return

    # Check for collisions with itself
    for segment in snake_body:
        if head.x == segment.x and head.y == segment.y:
            game_over = True
            return

    # Check for collision with food
    if head.x == food.x and head.y == food.y:
        snake_body.append(Segment(food.x, food.y))
        food.x = random.randint(0, COLS - 1) * TILE_SIZE
        food.y = random.randint(0, ROWS - 1) * TILE_SIZE
        score += 1

    # Update the snake's body segments
    for i in range(len(snake_body) - 1, -1, -1):
        segment = snake_body[i]
        if i == 0:
            segment.x = head.x
            segment.y = head.y
        else:
            segment.x = snake_body[i - 1].x
            segment.y = snake_body[i - 1].y

    # Move the snake head
    head.x += direction_x * TILE_SIZE
    head.y += direction_y * TILE_SIZE

def render():
    """Draw the game state on the canvas."""
    global head, food, snake_body, game_over, score
    update_game()

    canvas.delete("all")

    # Draw the food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill='red')

    # Draw the snake
    canvas.create_rectangle(head.x, head.y, head.x + TILE_SIZE, head.y + TILE_SIZE, fill='lime green')
    for segment in snake_body:
        canvas.create_rectangle(segment.x, segment.y, segment.x + TILE_SIZE, segment.y + TILE_SIZE, fill='lime green')

    # Draw game over or score text
    if game_over:
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Arial 20", text=f"Game Over: {score}", fill="white")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")

    # Schedule the next frame
    window.after(100, render)

render()
window.bind("<KeyRelease>", handle_key)
window.mainloop()
