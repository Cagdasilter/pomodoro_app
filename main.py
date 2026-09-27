import os
import tkinter as tk
from tkinter.ttk import Notebook


# ---------------------------- SETTINGS ---------------------------- #

WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 25

# Use True to test quickly.
# Use False for normal 25/5/25 minute Pomodoro times.
TEST_MODE = True

TEST_WORK_SECONDS = 10
TEST_SHORT_BREAK_SECONDS = 3
TEST_LONG_BREAK_SECONDS = 5

TOMATO_FILE = "tomato.png"

PLANT_FILES = [
    "tomato_stage_1.png",
    "tomato_stage_2.png",
    "tomato_stage_3.png",
    "tomato_stage_4.png",
    "tomato_stage_5.png",
    "tomato_stage_6.png",
]

PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Arial"


# ---------------------------- TIMER STATE ---------------------------- #

timer = None
current_mode = None
work_sessions_completed = 0
plant_stage = 1
block_started = False


def get_duration(minutes, test_seconds):
    if TEST_MODE:
        return test_seconds

    return minutes * 60


# ---------------------------- PLANT ---------------------------- #

def update_plant():
    forest_canvas.itemconfig(
        plant_image_item,
        image=plant_images[plant_stage - 1]
    )

    forest_progress_label.config(
        text=f"Work sessions completed: {work_sessions_completed}/5"
    )


# ---------------------------- TIMER ---------------------------- #

def start_timer():
    global block_started
    global work_sessions_completed
    global plant_stage

    if timer is not None:
        return

    if not block_started:
        block_started = True
        work_sessions_completed = 0
        plant_stage = 1
        update_plant()

    start_button.config(state=tk.DISABLED)
    start_work_session()


def start_work_session():
    global current_mode

    current_mode = "work"
    title_label.config(text="Work", fg=GREEN)

    count_down(
        get_duration(WORK_MIN, TEST_WORK_SECONDS)
    )


def start_short_break():
    global current_mode

    current_mode = "short_break"
    title_label.config(text="Short Break", fg=PINK)

    count_down(
        get_duration(SHORT_BREAK_MIN, TEST_SHORT_BREAK_SECONDS)
    )


def start_long_break():
    global current_mode

    current_mode = "long_break"
    title_label.config(text="Long Break", fg=RED)

    count_down(
        get_duration(LONG_BREAK_MIN, TEST_LONG_BREAK_SECONDS)
    )


def count_down(seconds_left):
    global timer

    minutes, seconds = divmod(seconds_left, 60)

    tomato_canvas.itemconfig(
        timer_text_item,
        text=f"{minutes:02d}:{seconds:02d}"
    )

    if seconds_left > 0:
        timer = window.after(
            1000,
            count_down,
            seconds_left - 1
        )
    else:
        timer = None
        finish_timer()


def finish_timer():
    global work_sessions_completed
    global plant_stage
    global current_mode
    global block_started

    if current_mode == "work":
        # Upgrade the plant after a completed work session.
        work_sessions_completed += 1
        plant_stage = work_sessions_completed + 1

        update_plant()

        checkmark_label.config(
            text="✔" * work_sessions_completed
        )

        if work_sessions_completed < 5:
            start_short_break()
        else:
            start_long_break()

    elif current_mode == "short_break":
        # The plant stays unchanged during short breaks.
        start_work_session()

    elif current_mode == "long_break":
        current_mode = None
        block_started = False

        title_label.config(
            text="Block Complete!",
            fg=GREEN
        )

        tomato_canvas.itemconfig(
            timer_text_item,
            text="00:00"
        )

        start_button.config(
            state=tk.NORMAL
        )


def reset_timer():
    global timer
    global current_mode
    global work_sessions_completed
    global plant_stage
    global block_started

    if timer is not None:
        window.after_cancel(timer)
        timer = None

    current_mode = None
    work_sessions_completed = 0
    plant_stage = 1
    block_started = False

    title_label.config(
        text="Ready to Start?",
        fg=GREEN
    )

    tomato_canvas.itemconfig(
        timer_text_item,
        text="00:00"
    )

    checkmark_label.config(text="")
    start_button.config(state=tk.NORMAL)

    update_plant()


# ---------------------------- WINDOW ---------------------------- #

window = tk.Tk()
window.title("My Pomodoro Productivity App")
window.config(
    padx=40,
    pady=30,
    bg=YELLOW
)

image_folder = os.path.dirname(
    os.path.abspath(__file__)
)

tomato_img = tk.PhotoImage(
    file=os.path.join(image_folder, TOMATO_FILE)
)

plant_images = [
    tk.PhotoImage(
        file=os.path.join(image_folder, filename)
    )
    for filename in PLANT_FILES
]


# ---------------------------- TABS ---------------------------- #

notebook = Notebook(window)
notebook.grid(row=0, column=0)

pomodoro_frame = tk.Frame(
    notebook,
    bg=YELLOW
)

forest_frame = tk.Frame(
    notebook,
    bg=YELLOW
)

notebook.add(
    pomodoro_frame,
    text="Pomodoro"
)

notebook.add(
    forest_frame,
    text="Forest"
)


# ---------------------------- POMODORO TAB ---------------------------- #

title_label = tk.Label(
    pomodoro_frame,
    text="Ready to Start?",
    font=(FONT_NAME, 35, "bold"),
    fg=GREEN,
    bg=YELLOW
)

title_label.grid(
    row=0,
    column=1
)


# Your original tomato.png stays on the main screen.
tomato_canvas = tk.Canvas(
    pomodoro_frame,
    width=250,
    height=250,
    bg=YELLOW,
    highlightthickness=0
)

tomato_canvas.grid(
    row=1,
    column=1
)

tomato_canvas.create_image(
    125,
    125,
    image=tomato_img
)


# Timer displayed on top of tomato.png.
timer_text_item = tomato_canvas.create_text(
    125,
    140,
    text="00:00",
    fill="white",
    font=(FONT_NAME, 35, "bold")
)


start_button = tk.Button(
    pomodoro_frame,
    text="Start",
    width=10,
    command=start_timer
)

start_button.grid(
    row=3,
    column=0,
    pady=15
)


reset_button = tk.Button(
    pomodoro_frame,
    text="Reset",
    width=10,
    command=reset_timer
)

reset_button.grid(
    row=3,
    column=2,
    pady=15
)


checkmark_label = tk.Label(
    pomodoro_frame,
    text="",
    font=(FONT_NAME, 15, "bold"),
    fg=GREEN,
    bg=YELLOW
)

checkmark_label.grid(
    row=4,
    column=1
)


# ---------------------------- FOREST TAB ---------------------------- #

forest_title_label = tk.Label(
    forest_frame,
    text="Tomato Forest",
    font=(FONT_NAME, 35, "bold"),
    fg=GREEN,
    bg=YELLOW,

)

forest_title_label.grid(
    row=0,
    column=1,
    pady=(0, 10)
)

forest_date_label = tk.Label(
    forest_frame,
    text="09/27/2026",
    font=(FONT_NAME, 10, "bold"),
    fg=GREEN,
    bg=YELLOW,

)

forest_date_label.grid(
    row=2,
    column=0,
)

forest_motivation_label = tk.Label(
    forest_frame,
    text="Keep Going!",
    font=(FONT_NAME, 10, "bold"),
    fg=GREEN,
    bg=YELLOW,

)

forest_motivation_label.grid(
    row=2,
    column=2,
)


forest_canvas = tk.Canvas(
    forest_frame,
    width=300,
    height=300,
    bg=YELLOW,
    highlightthickness=0
)

forest_canvas.grid(
    row=1,
    column=1
)


plant_image_item = forest_canvas.create_image(
    150,
    150,
    image=plant_images[0]
)


forest_progress_label = tk.Label(
    forest_frame,
    text="Work sessions completed: 0/5",
    font=(FONT_NAME, 13),
    fg="black",
    bg=YELLOW
)

forest_progress_label.grid(
    row=2,
    column=1,
    pady=(10, 0)
)


window.mainloop()