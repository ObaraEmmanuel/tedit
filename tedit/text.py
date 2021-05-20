import tkinter as tk


class TextArea(tk.Text):
    
    def __init__(self, master, **kw):
        cnf = {"undo": True, "maxundo": -1, "autoseparators": True, **kw}
        super(TextArea, self).__init__(master, cnf)
        self.bind("<<Modified>>", self._on_change)
        self.bind("<Control-z>", lambda _: self.edit_undo())
        self.bind("<Control-y>", lambda _: self.edit_redo())

    def _on_change(self, *_):
        flag = self.edit_modified()
        # skip possible implicit modifications
        if flag:
            self.event_generate("<<TextChange>>")
        self.edit_modified(False)

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
