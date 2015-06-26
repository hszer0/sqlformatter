import sqlparse
import re
import tkinter as tk
from pygments import lex
from pygments.lexers import sql

operatorspaceafter = r"""[=*><!+\-/]+[^ =*<>!+\-/]"""
operatorspacebefore = r"""[^ =*<>!+\-/][=*><!+\-/]+"""
endoperator = r"""[=*><!+\-/]+$"""
keywords = ['select', 'update', 'insert', 'create', 'create', 'drop', 'alter']


def format(s):
    if s is None:
        return ""
    parsedsql = sqlparse.format(s, reindent=True, keyword_case='upper')
    parts = parsedsql.split("'")

    for i in range(0, len(parts), 2):
        spacing = 0
        for match in re.finditer(operatorspacebefore, parts[i]):
            spacing += 1
            parts[i] = parts[i][
                :match.start() + spacing] + ' ' + parts[i][match.start() + spacing:]
        spacing = 0
        for match in re.finditer(operatorspaceafter, parts[i]):
            spacing += 1
            parts[i] = parts[i][
                :match.end() - 2 + spacing] + ' ' + parts[i][match.end() - 2 + spacing:]
        if (re.search(endoperator, parts[i])):
            parts[i] += ' '
    return "'".join(parts)


class GUI:

    def __init__(self):
        self.tk = tk.Tk()
        self.tk.resizable(0, 0)
        self.tk.title('SQL Formatter')
        self.last_content = ''
        self.tk.after(100, self.watch_clipboard)
        self.tk.text = tk.Text(self.tk, height=30, width=60)
        self.tk.text.tag_configure(
            "Token.Comment.Single", foreground="#036703")
        self.tk.text.tag_configure(
            "Token.Comment.Multiline", foreground="#036703")
        self.tk.text.tag_configure(
            "Token.Literal.String.Single", foreground="#FF0000")
        self.tk.text.tag_configure("Token.Keyword", foreground="#0000FF")
        self.tk.text.tag_configure("Token.Name.Builtin", foreground="#0000FF")
        self.tk.text.pack()
        self.tk.button = tk.Button(
            self.tk, text="Copy Formatted Query", command=self.copy_min)
        self.tk.button.pack()
        self.tk.text.config(state=tk.DISABLED)
        self.tk.attributes("-alpha", 0.85)
        self.tk.mainloop()

    def watch_clipboard(self):
        self.tk.text.config(state=tk.NORMAL)
        try:
            content = self.tk.clipboard_get()
            if any(keyword in content.lower() for keyword in keywords):
                if content != self.last_content:
                    self.last_content = content
                    newtext = format(content)
                    self.tk.text.delete(1.0, tk.END)
                    for token, content in lex(newtext, sql.SqlLexer()):
                        self.tk.text.insert(tk.END, content, str(token))
                    self.tk.clipboard_clear()
                    self.tk.clipboard_append(newtext)
                    self.tk.wm_state('normal')
                    self.tk.focus_force()
            else:
                self.tk.text.delete(1.0, tk.END)
        except:
            pass
        self.tk.text.config(state=tk.DISABLED)
        self.tk.after(500, self.watch_clipboard)

    def copy_min(self):
        self.tk.text.config(state=tk.NORMAL)
        content = self.tk.text.get(1.0, tk.END)
        self.last_content = content
        self.tk.clipboard_clear()
        self.tk.clipboard_append(content)
        self.tk.text.config(state=tk.DISABLED)
        self.tk.wm_state('iconic')


if __name__ == '__main__':
    gui = GUI()
