"""App that tracks and analyzes your time. """
from datetime import datetime
from functools import partial
import sys
import tkinter as tk
from tkinter import ttk
from typing import Any, Iterable
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
    _next_id = 0
    _subscribers = []

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # set button callback and bind tooltip methods
        self.tooltip = None
        self.bind("<Enter>", lambda _: self.show_tooltip())
        self.bind("<Leave>", lambda _: self.hide_tooltip())
        if self['command']:
            warnings.warn('ResponseButton will override command.')
        self['command'] = self.update_response

        # populate response data fields
        self.but_id, self._next_id = self._next_id, self._next_id + 1
        self.time = datetime.now().time().strftime('%H:%M:%S')
        self.resp = None
        self.update_response()

    def update_response(self) -> None:
        """Prompt user for a new response and update. """
        old_resp = self.resp
        self.resp = get_user_input()
        self['bg'] = CHOICE_COLOR[self.resp]
        self.notify_subscribers(old_resp, self.resp)

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

    @classmethod
    def register_subscriber(cls, new_sub: Any) -> None:
        """Register subscriber to notify when creating/updating buttons.

        Args:
            new_sub (Any): subscriber to update
        """
        cls._subscribers.append(new_sub)

    @classmethod
    def notify_subscribers(
        cls,
        old_resp: str,
        new_resp: str
    ) -> None:
        """Notify all subscribers of a button create/update event.

        Args:
            old_resp (str): old button user response
            new_resp (str): new button user response
        """
        for sub in cls._subscribers:
            sub.update(old_resp, new_resp)

    @property
    def data(self) -> str:
        """str: stored user response """
        return self.resp


class ResponseGraph:
    """Dynamic graph that tallies user response running total. """
    def __init__(self, dashboard: tk.Tk) -> None:
        self.fig, self.axes = plt.subplots(figsize=(4, 4))
        self.axes.set_facecolor('#333333')
        self.axes.set_title('Response Tally')
        self.canvas = FigureCanvasTkAgg(self.fig, dashboard)
        self.canvas.get_tk_widget().pack(padx=2, pady=2)
        self.bars = {curr: 0 for curr in CHOICES}
        self.draw()

    def update(
        self,
        old_resp: str,
        new_resp: str
    ) -> None:
        """Update response counts and redraw bar graph.

        Args:
            old_resp (str): old button user response
            new_resp (str): new button user response
        """
        if old_resp:
            self.bars[old_resp] -= 1  # not needed for new buttons
        self.bars[new_resp] += 1
        self.draw()

    def draw(self) -> None:
        """Clear and redraw bar graph. """
        self.axes.clear()
        bar_height = [self.bars[curr] for curr in CHOICES]
        bar_color = [CHOICE_COLOR[curr] for curr in CHOICES]
        self.axes.bar(CHOICES, bar_height, color=bar_color)
        self.canvas.draw()


if __name__ == '__main__':
    # Create progress tracker window
    root = tk.Tk()
    root.title('Progress')
    root_buttons = []

    # Initialize response tally
    graph = ResponseGraph(root)
    ResponseButton.register_subscriber(graph)

    try:
        for _ in range(5):
            # Pack user input into progress tracker
            but = ResponseButton(root, width=5, height=2)
            but.pack(padx=20, pady=0)
            root_buttons.append(but)

        root.mainloop()
    except tk.TclError as exc:
        print(f'Oops - {exc}')
        sys.exit()
