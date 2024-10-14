import tkinter as tk
import time
import pygame  # For sound notifications (cross-platform)

class Stopwatch:
    def __init__(self, master):
        self.master = master
        self.master.title("Stopwatch")

        self.is_running = False
        self.time_elapsed = 0
        self.target_time = 0
        self.notify_percentage = 0
        self.start_time = 0
        self.lap_number = 1
        self.lap_times = []

        # Initialize pygame for sound
        pygame.mixer.init()

        # Create a frame for the stopwatch display
        self.frame = tk.Frame(master)
        self.frame.pack(pady=20)

        self.time_label = tk.Label(self.frame, font=('calibri', 40, 'bold'), bg='black', fg='white')
        self.time_label.pack()

        # Create a frame for lap times with scrollbar
        self.lap_frame = tk.Frame(master)
        self.lap_frame.pack(pady=20)

        self.canvas = tk.Canvas(self.lap_frame)
        self.scrollbar = tk.Scrollbar(self.lap_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.lap_label = tk.Label(self.scrollable_frame, font=('calibri', 20), text="Lap Times:")
        self.lap_label.pack()

        self.lap_times_label = tk.Label(self.scrollable_frame, font=('calibri', 20), text="")
        self.lap_times_label.pack()

        # Control buttons
        self.button_frame = tk.Frame(master)
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(self.button_frame, text='Start', command=self.start, font=('calibri', 20), width=10)
        self.start_button.pack(side='left', padx=10)

        self.stop_button = tk.Button(self.button_frame, text='Stop', command=self.stop, font=('calibri', 20), width=10)
        self.stop_button.pack(side='left', padx=10)

        self.reset_button = tk.Button(self.button_frame, text='Reset', command=self.reset, font=('calibri', 20), width=10)
        self.reset_button.pack(side='left', padx=10)

        self.lap_button = tk.Button(self.button_frame, text='Lap', command=self.lap, font=('calibri', 20), width=10)
        self.lap_button.pack(side='left', padx=10)

        # User input for target time
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(pady=20)

        self.hours_label = tk.Label(self.input_frame, text="Hours:", font=('calibri', 14))
        self.hours_label.pack(side='left')

        self.hours_entry = tk.Entry(self.input_frame, font=('calibri', 14), width=5)
        self.hours_entry.pack(side='left', padx=5)

        self.minutes_label = tk.Label(self.input_frame, text="Minutes:", font=('calibri', 14))
        self.minutes_label.pack(side='left')

        self.minutes_entry = tk.Entry(self.input_frame, font=('calibri', 14), width=5)
        self.minutes_entry.pack(side='left', padx=5)

        self.seconds_label = tk.Label(self.input_frame, text="Seconds:", font=('calibri', 14))
        self.seconds_label.pack(side='left')

        self.seconds_entry = tk.Entry(self.input_frame, font=('calibri', 14), width=5)
        self.seconds_entry.pack(side='left', padx=5)

        self.target_label = tk.Label(self.input_frame, text="Target Time:", font=('calibri', 14))
        self.target_label.pack(side='left')

        self.target_entry = tk.Label(self.input_frame, text="00:00:00", font=('calibri', 14))
        self.target_entry.pack(side='left', padx=5)

        self.notify_label = tk.Label(self.input_frame, text="Notify at (%):", font=('calibri', 14))
        self.notify_label.pack(side='left')

        self.notify_entry = tk.Entry(self.input_frame, font=('calibri', 14), width=5)
        self.notify_entry.pack(side='left', padx=5)

        self.update_button = tk.Button(self.input_frame, text="Update", command=self.update_target_time, font=('calibri', 14))
        self.update_button.pack(side='left', padx=5)

        self.update_clock()

    def update_clock(self):
        if self.is_running:
            current_time = time.time()
            self.time_elapsed = current_time - self.start_time

            hours, remainder = divmod(int(self.time_elapsed), 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int((self.time_elapsed - int(self.time_elapsed)) * 1000)
            self.time_label.config(text=f'{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}')

            # Check for notifications
            if self.target_time > 0:
                if self.time_elapsed >= self.target_time:
                    self.notify("Target time reached!", True)
                    self.reset()
                elif self.notify_percentage > 0 and self.time_elapsed >= (self.notify_percentage / 100) * self.target_time:
                    self.notify(f"{self.notify_percentage}% of target time completed!", True)
                    self.notify_percentage = 0  # Reset notification after displaying it

            self.master.after(10, self.update_clock)  # Update every 10 milliseconds for smoother display

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = time.time() - self.time_elapsed  # Ensure resumed time is correct
            try:
                # Get target time from separate fields
                hours_value = int(self.hours_entry.get()) if self.hours_entry.get() else 0
                minutes_value = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
                seconds_value = int(self.seconds_entry.get()) if self.seconds_entry.get() else 0

                # Combine into total target time in seconds
                self.target_time = hours_value * 3600 + minutes_value * 60 + seconds_value

                self.notify_percentage = int(self.notify_entry.get()) if self.notify_entry.get() else 0
            except ValueError:
                self.notify("Please enter valid integers for time and notification percentage.", False)
                return
            self.update_clock()  # Start updating the clock when the timer starts

    def stop(self):
        if self.is_running:
            self.is_running = False

    def reset(self):
        self.is_running = False
        self.time_elapsed = 0
        self.time_label.config(text='00:00:00.000')
        self.lap_number = 1
        self.lap_times = []
        self.lap_times_label.config(text="")
        # Clear input fields
        self.hours_entry.delete(0, tk.END)
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.notify_entry.delete(0, tk.END)

    def lap(self):
        if self.is_running:
            lap_time = time.time() - self.start_time
            hours, remainder = divmod(int(lap_time), 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int((lap_time - int(lap_time)) * 1000)
            lap_time_str = f'Lap {self.lap_number}: {hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}'
            self.lap_times.append(lap_time_str)
            self.lap_times_label.config(text="\n".join(self.lap_times))
            self.lap_number += 1

    def notify(self, message, play_sound=False):
        alert_window = tk.Toplevel(self.master)
        alert_window.title("Notification")
        alert_label = tk.Label(alert_window, text=message, font=('calibri', 20))
        alert_label.pack(pady=20)
        ok_button = tk.Button(alert_window, text="OK", command=alert_window.destroy, font=('calibri', 15))
        ok_button.pack(pady=10)

        if play_sound:
            # Play a sound notification using pygame
            pygame.mixer.music.load("notify.wav")  # Replace with the path to your sound file
            pygame.mixer.music.play()

    def update_target_time(self):
        # Update the target time label based on the input fields
        hours_value = int(self.hours_entry.get()) if self.hours_entry.get() else 0
        minutes_value = int(self.minutes_entry.get()) if self.minutes_entry.get() else 0
        seconds_value = int(self.seconds_entry.get()) if self.seconds_entry.get() else 0

        total_seconds = hours_value * 3600 + minutes_value * 60 + seconds_value
        self.target_entry.config(text=f"{hours_value:02}:{minutes_value:02}:{seconds_value:02}")

if __name__ == "__main__":
    root = tk.Tk()
    stopwatch = Stopwatch(root)
    root.mainloop()
