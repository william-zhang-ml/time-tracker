"""App that tracks and analyzes your time. """
from functools import partial
import tkinter as tk


__author__ = 'William Zhang'


def print_value(var: tk.StringVar) -> None:
    """Print the value stored in a variable.

    Args:
        var (tk.StringVar): tkinter string variable
    """
    print(f'Radio out -> {var.get()}')


if __name__ == '__main__':
    # Create main window
    root = tk.Tk()
    root.title('Check-in')

    # Build check-in form
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    choices = ['Option 1', 'Option 2', 'Option 3']
    radio_out = tk.StringVar(value=choices[0])
    for choice in choices:
        radio = tk.Radiobutton(
            frame,
            text=choice,
            variable=radio_out,
            value=choice
        )
        radio.pack(padx=20, pady=5)
    submit = tk.Button(
        root,
        text='Submit',
        command=partial(print_value, radio_out)
    )
    submit.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()
