"""App that tracks and analyzes your time. """
from collections import Counter
from datetime import datetime
from functools import partial
import sys
import tkinter as tk
from tkinter import ttk
from typing import Iterable
import warnings
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
CHOICE_COLOR = {
    'Option 1': '#baffc9',
    'Option 2': '#bae1ff',
    'Option 3': '#ffb3ba'
}
get_user_input = partial(open_choice_menu, CHOICES)


class ResponseButton(tk.Button):
    """Button that keeps track of user response, lets user change response. """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bind("<Enter>", lambda _: self.show_tooltip())
        self.bind("<Leave>", lambda _: self.hide_tooltip())
        self.time = datetime.now().time().strftime('%H:%M:%S')
        self.tooltip = None
        if self['command']:
            warnings.warn('ResponseButton will override command.')
        self['command'] = self.update_response
        self.update_response()

    def update_response(self) -> None:
        """Prompt user for a new response and update. """
        self.resp = get_user_input()
        self['bg'] = CHOICE_COLOR[self.resp]

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
            text=f'{self.time} -> {self.resp}',
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

    @property
    def data(self) -> str:
        """str: stored user response """
        return self.resp


if __name__ == '__main__':
    # Create progress tracker window
    root = tk.Tk()
    root.title('Progress')
    root_buttons = []

    try:
        for _ in range(5):
            # Pack user input into progress tracker
            but = ResponseButton(root, width=5, height=2)
            but.pack(padx=20, pady=0)
            root_buttons.append(but)

        # Show initial response summary in a bar graph
        counter = Counter([but.data for but in root_buttons])
        bar_height = []
        for curr in CHOICES:
            bar_height.append(counter[curr])
        fig, axes = plt.subplots(figsize=(4, 4))
        axes.bar(CHOICES, bar_height, color=CHOICE_COLOR.values())
        axes.set_facecolor('#333333')
        axes.set_title('Initial response summary')
        canvas = FigureCanvasTkAgg(fig, root)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=2, pady=2)

        root.mainloop()
    except tk.TclError as exc:
        print(f'Oops - {exc}')
        sys.exit()
