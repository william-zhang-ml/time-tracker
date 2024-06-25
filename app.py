"""App that tracks and analyzes your time. """
import tkinter as tk
from tkinter import ttk
from typing import List


__author__ = 'William Zhang'


def get_user_input(choices: List[str]) -> str:
    """Get user input via a multiple choice question window.

    Args:
        choices (List[str]): choices for the user to select

    Returns:
        str: user selection
    """
    window = tk.Toplevel()
    window.title('Check-in')
    radio_out = tk.StringVar(value=choices[0])
    for choice in choices:
        radio = ttk.Radiobutton(
            window,
            text=choice,
            variable=radio_out,
            value=choice
        )
        radio.pack(padx=20, pady=5)
    submit = ttk.Button(
        window,
        text='Submit',
        command=window.destroy
    )
    submit.pack(pady=10)
    window.wait_window()
    return radio_out.get()


if __name__ == '__main__':
    # Create main window
    root = tk.Tk()
    root.title('Progress')
    root.withdraw()

    # Get user input
    resp = get_user_input(['Option 1', 'Option 2', 'Option 3'])
    print(resp)

    # Destroy the main window
    root.destroy()
