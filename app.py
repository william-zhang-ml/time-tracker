"""App that tracks and analyzes your time. """
from functools import partial
import sys
import tkinter as tk
from tkinter import ttk
from typing import Iterable
import warnings


__author__ = 'William Zhang'


def open_choice_menu(choices: Iterable[str]) -> str:
    """Get user input via a multiple choice question window.

    Args:
        choices (Iterable[str]): choices for the user to select

    Returns:
        str: user selection
    """
    window = tk.Toplevel()
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


CHOICES = ['Option 1', 'Option 2', 'Option 3']
get_user_input = partial(open_choice_menu, CHOICES)


class ResponseButton(ttk.Button):
    """Button that keeps track of user response, lets user change response. """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", lambda _: self.show_tooltip())
        self.bind("<Leave>", lambda _: self.hide_tooltip())
        self.tooltip = None
        if self['command']:
            warnings.warn('ResponseButton will override command.')
        self['command'] = self.update_response

    def update_response(self) -> None:
        """Prompt user for a new response and update. """
        self['text'] = get_user_input()

    def show_tooltip(self) -> None:
        """Create a new tooltip window. """
        if self.tooltip:
            return  # already activated
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(1)
        self.tooltip.wm_geometry(
            f'+{self.winfo_rootx()}+{self.winfo_rooty() + 25}'
        )
        label = ttk.Label(
            self.tooltip,
            text=self.cget('text'),
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1
        )
        label.pack(ipadx=1)

    def hide_tooltip(self) -> None:
        """Destroy the tooltip window. """
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


if __name__ == '__main__':
    # Create progress tracker window
    root = tk.Tk()
    root.title('Progress')

    try:
        for _ in range(5):
            # Get user input
            resp = get_user_input()

            # Pack into progress tracker
            but = ResponseButton(root, text=resp)
            but.pack(padx=20, pady=5)

        root.mainloop()
    except tk.TclError:
        sys.exit()
