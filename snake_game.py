from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 200
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOUR = "GREEN"
FOOD_COLOUR = "RED"
BACKGROUND_COLOUR = "BLACK"

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])

            for x, y in self.coordinates:
                square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR, tags="snake")
                self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) -1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x,y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = FOOD_COLOUR, tag = "food")

def next_turn(snake, food):
    global score, GAME_WIDTH, GAME_HEIGHT

    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOUR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

        # Decrease the size of the game board
        GAME_WIDTH -= SPACE_SIZE
        GAME_HEIGHT -= SPACE_SIZE
        canvas.config(width=GAME_WIDTH, height=GAME_HEIGHT)

        # Decrease the size of the death border
        for item in canvas.find_all():
            if canvas.type(item) == "rectangle" and canvas.itemcget(item, "fill") == "white":
                x1, y1, x2, y2 = canvas.coords(item)
                canvas.coords(item, x1 + SPACE_SIZE, y1 + SPACE_SIZE, x2 - SPACE_SIZE, y2 - SPACE_SIZE)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

    # Always spawn food after each turn within the adjusted boundaries
    if GAME_WIDTH > SPACE_SIZE and GAME_HEIGHT > SPACE_SIZE and not canvas.find_withtag("food"):
        food = Food()




def change_directions(new_direction):

    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True


    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print('game over')
            return True

    return False
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text="GAME OVER", fill="red", tag="gameover")

window = Tk()
window.title("Snake Game")
window.resizable(False,False)


score = 0
direction = 'down'

label = Label(window, text = 'Score{}'.format(score), font=('consolas', 40))
label.pack()


canvas = Canvas(window, bg=BACKGROUND_COLOUR, height=GAME_HEIGHT, width= GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_hight = window.winfo_screenheight()

x = int((screen_width/2) -(window_width/2))
y = int((screen_hight/2) -(window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")


window.bind('<Left>', lambda event: change_directions('left'))
window.bind('<Right>', lambda event: change_directions('right'))
window.bind('<Up>', lambda event: change_directions('up'))
window.bind('<Down>', lambda event: change_directions('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()