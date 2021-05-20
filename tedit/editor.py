from tkinter import Frame, ttk

from tedit.text import TextArea, LineNumbers


class Editor(Frame):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.gutter = Frame(self, bg="#353535")
        self.text = TextArea(self)
        self.text.bind("<<TextChange>>", self._on_change)
        self.x_scroll = ttk.Scrollbar(self, orient="horizontal")
        self.y_scroll = ttk.Scrollbar(self, orient="vertical")
        self.gutter.grid(row=0, column=0, sticky='nswe')
        self.line_numbers = LineNumbers(self.gutter)
        self.line_numbers.pack(fill="both", expand=True)
        self.text.grid(row=0, column=1)
        self.y_scroll.grid(row=0, column=2, sticky='ns')
        self.x_scroll.grid(row=1, column=1, sticky='ew')
        self.columnconfigure(1, uniform=1)
        self.text.configure(
            yscrollcommand=self._set_scroll_y,
            xscrollcommand=self._set_scroll_x
        )
        self.line_numbers.configure(yscrollcommand=self._set_line_number_scroll)
        self.x_scroll.configure(command=self._scroll_x)
        self.y_scroll.configure(command=self._scroll_y)

    def _on_change(self, _):
        self.line_numbers.update_numbers(self.text)

    def _scroll_x(self, *args):
        self.text.xview(*args)

    def _scroll_y(self, *args):
        self.text.yview(*args)
        self.line_numbers.yview(*args)

    def _set_scroll_x(self, *args):
        if args == ('0.0', '1.0'):
            if self.x_scroll.winfo_ismapped():
                self.x_scroll.grid_forget()
        elif not self.x_scroll.winfo_ismapped():
            self.x_scroll.grid(row=1, column=1, sticky='ew')
        self.x_scroll.set(*args)

    def _set_scroll_y(self, *args):
        if args == ('0.0', '1.0'):
            if self.y_scroll.winfo_ismapped():
                self.y_scroll.grid_forget()
        elif not self.y_scroll.winfo_ismapped():
            self.y_scroll.grid(row=0, column=2, sticky='ns')

        if self.line_numbers.yview() != self.text.yview():
            self.line_numbers.yview_moveto(args[0])
        self.y_scroll.set(*args)

    def _set_line_number_scroll(self, *args):
        if self.text.yview() != self.line_numbers.yview():
            self.text.yview_moveto(args[0])
        self.y_scroll.set(*args)

