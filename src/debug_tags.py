#!/usr/bin/env python3
"""Find first tag imbalance position in index.html and show context."""
import html.parser
import sys

class P(html.parser.HTMLParser):
    VOID = {"br", "img", "hr", "meta", "link", "input", "source"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.first_err = None
    def handle_starttag(self, t, a):
        if t not in self.VOID:
            self.stack.append((t, self.getpos()[0]))
    def handle_endtag(self, t):
        if t in self.VOID:
            return
        if self.stack and self.stack[-1][0] == t:
            self.stack.pop()
        elif self.first_err is None:
            self.first_err = (t, self.getpos()[0], list(self.stack[-4:]))

src = open(sys.argv[1]).read()
p = P()
p.feed(src)
if p.first_err:
    t, line, tail = p.first_err
    print(f"FIRST ERROR: </{t}> at line {line}; stack tail {tail}")
    lines = src.split("\n")
    lo, hi = max(0, line - 6), min(len(lines), line + 2)
    for ln in range(lo, hi):
        print(f"{ln+1:5d}| {lines[ln][:400]}")
else:
    print("balanced")
