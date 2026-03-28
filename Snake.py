import turtle
import time
import random
import os

WIDTH = 600
HEIGHT = 600
STEP = 20

# ---------- HIGH SCORE LOAD ----------
if os.path.exists("highscore.txt"):
    with open("highscore.txt","r") as f:
        high_score = int(f.read())
else:
    high_score = 0

score = 0

# ---------- SCREEN ----------
wn = turtle.Screen()
wn.title("Arcade Snake")
wn.bgcolor("#020617")
wn.setup(width=WIDTH, height=HEIGHT)
wn.tracer(0)

# ---------- GRID ----------
grid = turtle.Turtle()
grid.hideturtle()
grid.speed(0)
grid.color("#1e293b")

for i in range(-300,301,20):
    grid.penup()
    grid.goto(i,-300)
    grid.pendown()
    grid.goto(i,300)

for i in range(-300,301,20):
    grid.penup()
    grid.goto(-300,i)
    grid.pendown()
    grid.goto(300,i)

# ---------- WALL ----------
wall = turtle.Turtle()
wall.hideturtle()
wall.pensize(6)
wall.color("#ef4444")

wall.penup()
wall.goto(-290,-290)
wall.pendown()

for _ in range(4):
    wall.forward(580)
    wall.left(90)

# ---------- SCORE DISPLAY ----------
score_pen = turtle.Turtle()
score_pen.hideturtle()
score_pen.penup()
score_pen.color("white")
score_pen.goto(0,260)

# ---------- UI ----------
ui = turtle.Turtle()
ui.hideturtle()
ui.penup()
ui.color("#22d3ee")

# ---------- SNAKE ----------
head = turtle.Turtle()
head.shape("square")
head.color("#22c55e")
head.penup()
head.direction = "stop"
head.hideturtle()

segments = []

# ---------- FOOD ----------
food = turtle.Turtle()
food.shape("circle")
food.color("#f43f5e")
food.penup()
food.goto(1000,1000)
food.hideturtle()

# ---------- GAME STATE ----------
game_running = False
paused = False
delay = 0.1

# ---------- FUNCTIONS ----------

def update_score():
    score_pen.clear()
    score_pen.write(
        f"Score: {score}   High Score: {high_score}",
        align="center",
        font=("Courier",18,"bold")
    )

def save_high_score():
    with open("highscore.txt","w") as f:
        f.write(str(high_score))

def spawn_food():

    while True:

        x = random.randrange(-260,260,20)
        y = random.randrange(-260,260,20)

        overlap = False

        if abs(head.xcor()-x) < 20 and abs(head.ycor()-y) < 20:
            overlap = True

        for seg in segments:
            if abs(seg.xcor()-x) < 20 and abs(seg.ycor()-y) < 20:
                overlap = True
                break

        if not overlap:
            break

    food.goto(x,y)
    food.showturtle()

def start_game():

    global game_running, score, paused, delay

    ui.clear()

    score = 0
    paused = False
    delay = 0.1
    game_running = True

    head.goto(0,0)
    head.direction = "stop"
    head.showturtle()

    for s in segments:
        s.goto(1000,1000)

    segments.clear()

    spawn_food()
    update_score()

def toggle_pause():

    global paused

    if not game_running:
        return

    paused = not paused

    ui.clear()

    if paused:
        ui.write(
            "PAUSED",
            align="center",
            font=("Courier",28,"bold")
        )

def game_over():

    global game_running, high_score

    game_running = False
    food.hideturtle()

    if score > high_score:
        high_score = score
        save_high_score()

    ui.clear()
    ui.write(
        "GAME OVER\nPress SPACE",
        align="center",
        font=("Courier",28,"bold")
    )

def move():

    if head.direction == "up":
        head.sety(head.ycor()+STEP)

    if head.direction == "down":
        head.sety(head.ycor()-STEP)

    if head.direction == "left":
        head.setx(head.xcor()-STEP)

    if head.direction == "right":
        head.setx(head.xcor()+STEP)

# ---------- CONTROLS ----------

def go_up():
    if head.direction!="down":
        head.direction="up"

def go_down():
    if head.direction!="up":
        head.direction="down"

def go_left():
    if head.direction!="right":
        head.direction="left"

def go_right():
    if head.direction!="left":
        head.direction="right"

wn.listen()

wn.onkeypress(go_up,"Up")
wn.onkeypress(go_down,"Down")
wn.onkeypress(go_left,"Left")
wn.onkeypress(go_right,"Right")

wn.onkeypress(start_game,"space")
wn.onkeypress(toggle_pause,"p")

# ---------- START SCREEN ----------

ui.write(
    "ARCADE SNAKE\nPress SPACE",
    align="center",
    font=("Courier",28,"bold")
)

update_score()

# ---------- GAME LOOP ----------

while True:

    wn.update()

    if paused:
        continue

    if game_running:

        # move body
        for i in range(len(segments)-1,0,-1):

            x = segments[i-1].xcor()
            y = segments[i-1].ycor()

            segments[i].goto(x,y)

        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()

        # wall collision
        if abs(head.xcor())>280 or abs(head.ycor())>280:
            game_over()

        # food collision
        if head.distance(food) < 15:

            food.hideturtle()

            segment = turtle.Turtle()
            segment.shape("square")
            segment.color("#4ade80")
            segment.penup()
            segment.goto(1000,1000)
            segments.append(segment)

            score += 10

            update_score()

            spawn_food()

            if delay > 0.05:
                delay -= 0.002

        # self collision
        for seg in segments:
            if seg.distance(head) < 10:
                game_over()

        time.sleep(delay)

wn.mainloop()