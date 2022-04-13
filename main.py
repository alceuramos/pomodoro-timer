from re import T
import time
import math
import threading
import tkinter as tk
from tkinter import ttk, PhotoImage

POMODORO_MINUTES = 30
SHORT_REST_MINUTES = 5
LONG_REST_MINUTES = 10

SMALL_FONT = ("Ubuntu", 12)
TOMATO_TEXT = ''

class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        # self.root.geometry("350x150")
        self.root.title("Pomodoro Timer [insert some tomato here]")
        # tomato = PhotoImage(file="tomato.png")
        # self.root.tk.call('wm','iconphoto', self.root._w, tomato)

        self.s = ttk.Style()
        self.s.configure("TNotebook.Tab", font=SMALL_FONT)
        self.s.configure("TButton", font=SMALL_FONT)

        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(fill="both", pady=10, expand=True)

        self.tab1 = ttk.Frame(self.tabs)
        self.tab2 = ttk.Frame(self.tabs)
        self.tab3 = ttk.Frame(self.tabs)

        self.pomodoro_timer_label = ttk.Label(self.tab1, text=f"{POMODORO_MINUTES:02d}:00", font=("Ubuntu",48))
        self.pomodoro_timer_label.pack()

        self.short_rest_timer_label = ttk.Label(self.tab2, text=f"{SHORT_REST_MINUTES:02d}:00", font=("Ubuntu",48))
        self.short_rest_timer_label.pack()

        self.long_rest_timer_label = ttk.Label(self.tab3, text=f"{LONG_REST_MINUTES:02d}:00", font=("Ubuntu",48))
        self.long_rest_timer_label.pack()

        self.tabs.add(self.tab1, text="Pomodoro")
        self.tabs.add(self.tab2, text="Short Rest")
        self.tabs.add(self.tab3, text="Long Rest")


        self.grid_layout = ttk.Frame(self.root)
        self.grid_layout.pack(pady=(0,10),padx=10)

        self.pomodoro_counter_label = ttk.Label(self.grid_layout, text="Pomodoros: 0", font=SMALL_FONT)
        self.pomodoro_counter_label.grid(row=0, column=0, columnspan=4, pady=(0,10))

        self.start_button = ttk.Button(self.grid_layout, text="Start", command=self.start_timer_thread)
        self.start_button.grid(row=1, column=0)

        self.pause_button = ttk.Button(self.grid_layout, text="Pause", command=self.pause_timer)
        self.pause_button.grid(row=1, column=1)

        self.skip_button = ttk.Button(self.grid_layout, text="Skip", command=self.skip_timer)
        self.skip_button.grid(row=1, column=2)

        self.reset_button = ttk.Button(self.grid_layout, text="Reset", command=self.reset_timer)
        self.reset_button.grid(row=1, column=3)



        self.pomodoro_counter = 0
        self.skipped = False
        self.stopped = False
        self.running = False
        self.paused = False

        self.root.mainloop()

    def start_timer_thread(self):
        if not self.running:
            t = threading.Thread(target=self.start_timer)
            t.start()
            self.running = True
            self.paused = False

    def start_timer(self):
        self.stopped = False
        self.skipped = False
        self.paused = False
        timer_id = self.tabs.index(self.tabs.select())


        self.time_counter(timer_id)

            
        if not self.stopped or self.skipped:
            if timer_id == 0:
                self.pomodoro_counter += 1
                self.pomodoro_counter_label.configure(text=f"Pomodoros: {self.pomodoro_counter}")
                if self.pomodoro_counter % 4 == 0:
                    self.tabs.select(2)
                else:
                    self.tabs.select(1)
            elif timer_id == 1 or timer_id == 2:
                self.tabs.select(0)
            self.start_timer()

    def time_counter(self, timer_id):
        if timer_id == 0:
            full_seconds = 60 * POMODORO_MINUTES
        elif timer_id == 1:
            full_seconds = 60 * SHORT_REST_MINUTES
        elif timer_id == 2:
            full_seconds = 60 * LONG_REST_MINUTES
        while full_seconds > 0 and not self.stopped:

            if not self.paused:
                minutes, seconds = divmod(full_seconds,60)
                minutes = int(minutes)
                seconds = math.floor(seconds)

                time.sleep(0.1)
                full_seconds -= 0.1

                if timer_id == 0:
                    self.pomodoro_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                elif timer_id == 1:
                    self.short_rest_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                elif timer_id == 2:
                    self.long_rest_timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
                self.root.update()
        
        self.reset_labels()

    def pause_timer(self):
        self.paused = not self.paused


    def reset_timer(self):
        self.stopped = True
        self.skipped = False
        self.running = False
        self.paused = False

        self.pomodoro_counter = 0
        self.pomodoro_counter_label.configure(text="Pomodoros: 0")
        
        
        self.reset_labels()


    def skip_timer(self):
        
        self.skipped = True
        self.stopped = True
        self.paused = False
    
    def reset_labels(self):
        self.pomodoro_timer_label.configure(text=f"{POMODORO_MINUTES:02d}:00")
        self.short_rest_timer_label.configure(text=f"{SHORT_REST_MINUTES:02d}:00")     
        self.long_rest_timer_label.configure(text=f"{LONG_REST_MINUTES:02d}:00")
    
if __name__ == '__main__':
    PomodoroTimer()