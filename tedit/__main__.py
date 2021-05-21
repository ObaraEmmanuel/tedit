from tedit import Editor
from tkinter import Tk


if __name__ == "__main__":
    root = Tk()
    editor = Editor(root, width=400, height=350)
    editor.pack(fill="both", expand=1)
    editor.text.config_highlight(lexer="python", style="monokai", tab=4)
    root.mainloop()
