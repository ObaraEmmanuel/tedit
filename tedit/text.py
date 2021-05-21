import tkinter as tk
from tkinter.font import Font
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.lexer import Lexer

from tedit.formatter import TextFormatter


class TextArea(tk.Text):
    
    def __init__(self, master, **kw):
        cnf = dict(
            wrap=tk.NONE, relief=tk.FLAT, bd=0, bg="#202020",
            highlightthickness=0, fg="#f7f7f7", padx=5, pady=5,
            undo=True, maxundo=-1, autoseparators=True,
            insertbackground="#f7f7f7",
        )
        cnf.update(kw)
        super(TextArea, self).__init__(master, cnf)
        self.bind("<<Modified>>", self._on_change)
        self.bind("<Control-z>", lambda _: self.edit_undo())
        self.bind("<Control-y>", lambda _: self.edit_redo())
        self._lexer = get_lexer_by_name("python")
        self._formatter = TextFormatter(self, style="default")
        self._highlight_enabled = True

    def config_highlight(self, **options):
        if options.get("lexer") is not None:
            if isinstance(options['lexer'], Lexer):
                self._lexer = options['lexer']
            else:
                self._lexer = get_lexer_by_name(options['lexer'])

        if options.get("style") is not None:
            self._formatter = TextFormatter(self, style=options["style"])

        if options.get("tab"):
            tab_size = Font(font=self["font"]).measure(" "*options["tab"])
            self.configure(tabs=tab_size)

        self._highlight_enabled = options.get("highlight", True)

    def _on_change(self, *_):
        flag = self.edit_modified()
        # skip possible implicit modifications
        if flag:
            self.event_generate("<<TextChange>>")
            self._format()
        self.edit_modified(False)

    def _format(self):
        if self._highlight_enabled:
            highlight(self.get_all(), self._lexer, self._formatter)

    def get_all(self):
        return self.get("1.0", tk.END)

    def edit_undo(self):
        try:
            super(TextArea, self).edit_undo()
        except tk.TclError:
            # usually thrown when no more undo is available
            pass
        # suppress any external bindings
        return "break"

    def edit_redo(self):
        try:
            super(TextArea, self).edit_redo()
        except tk.TclError:
            pass
        # suppress any external bindings
        return "break"


class LineNumbers(tk.Text):

    def __init__(self, master, **kw):
        # defaults
        cnf = dict(
            bg="#353535", fg="#aaaaaa", width=3, relief=tk.FLAT, bd=0,
            highlightthickness=0, padx=5, pady=5, wrap=tk.NONE,
            selectbackground="#353535", selectforeground="#aaaaaa",
            exportselection=0, insertbackground="#353535",
            inactiveselectbackground="#353535", takefocus=False
        )
        cnf.update(kw, state=tk.DISABLED)
        super(LineNumbers, self).__init__(master, **cnf)
        self.insert(tk.END, "1")
        self._last = 1

    def insert(self, index, chars, *args):
        self.configure(state=tk.NORMAL)
        super(LineNumbers, self).insert(index, chars, *args)
        self.configure(state=tk.DISABLED)

    def delete(self, index1, index2=None):
        self.configure(state=tk.NORMAL)
        super(LineNumbers, self).delete(index1, index2)
        self.configure(state=tk.DISABLED)

    def update_numbers(self, text):
        line, _ = list(map(int, text.index(tk.END).split(".")))
        last, _ = list(map(int, self.index(tk.END).split(".")))
        if line == last:
            return

        if line > last:
            self.insert(tk.END, "\n")
            self.insert(tk.END, "\n".join(list(map(str, range(last, line)))))
        elif last > line:
            self.delete("{}.0".format(line), tk.END)
        self.configure(width=max(3, len(str(line - 1))))
