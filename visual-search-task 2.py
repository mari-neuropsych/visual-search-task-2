import tkinter as tk
import random
import time
import numpy as np

class VisualSearchTask:
    def __init__(self, master, trials=10, grid_size=5):
        self.master = master
        self.trials = trials
        self.grid_size = grid_size
        self.current_trial = 0
        self.results = []

        self.target_color = "red"
        self.distractor_colors = ["blue", "green", "yellow"]

        self.canvas = tk.Canvas(master, width=400, height=400, bg="white")
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.click_canvas)

        self.next_trial()

    def generate_synthetic_eeg(self, length=100):
        t = np.linspace(0, 1, length)
        signal = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(length)
        return signal

    def next_trial(self):
        if self.current_trial < self.trials:
            self.canvas.delete("all")
            self.start_time = time.time()
            self.current_eeg = self.generate_synthetic_eeg()

            self.cells = []
            self.target_position = (random.randint(0, self.grid_size-1),
                                    random.randint(0, self.grid_size-1))

            for i in range(self.grid_size):
                row = []
                for j in range(self.grid_size):
                    x1 = j * 70 + 10
                    y1 = i * 70 + 10
                    x2 = x1 + 50
                    y2 = y1 + 50
                    if (i,j) == self.target_position:
                        color = self.target_color
                    else:
                        color = random.choice(self.distractor_colors)
                    rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                    row.append(rect)
                self.cells.append(row)
        else:
            self.show_results()

    def click_canvas(self, event):
        col = event.x // 70
        row = event.y // 70
        clicked_correct = (row, col) == self.target_position
        reaction_time = time.time() - self.start_time
        self.results.append({
            "trial": self.current_trial + 1,
            "clicked_position": (row, col),
            "target_position": self.target_position,
            "correct": clicked_correct,
            "reaction_time": reaction_time,
            "eeg_signal": self.current_eeg.tolist()
        })
        self.current_trial += 1
        self.next_trial()

    def show_results(self):
        self.canvas.delete("all")
        self.canvas.create_text(200,200,text="Task Complete!", font=("Arial",24))
        print("Trial | Clicked Position | Target Position | Correct | Reaction Time")
        for r in self.results:
            print(f"{r['trial']} | {r['clicked_position']} | {r['target_position']} | {r['correct']} | {r['reaction_time']:.3f}s")
        print("\nSynthetic EEG data for each trial is available in 'eeg_signal' field.")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Visual Search Task")
    app = VisualSearchTask(root)
    root.mainloop()
