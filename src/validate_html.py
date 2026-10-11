#!/usr/bin/env python3
"""Validate site/index.html: tag balance + stats."""
import html.parser
import sys

class P(html.parser.HTMLParser):
    VOID = {"br", "img", "hr", "meta", "link", "input", "source"}
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.errs = []
    def handle_starttag(self, t, a):
        if t not in self.VOID:
            self.stack.append(t)
    def handle_endtag(self, t):
        if t in self.VOID:
            return
        if self.stack and self.stack[-1] == t:
            self.stack.pop()
        else:
            self.errs.append(
                f"mismatch </{t}> line {self.getpos()[0]}; stack tail {self.stack[-3:]}")

src = open(sys.argv[1] if len(sys.argv) > 1 else "site/index.html").read()
p = P()
p.feed(src)
print("tag-balance errors:", len(p.errs))
for e in p.errs[:12]:
    print("  ", e)
print("residual stack:", p.stack[:10])
print("bytes:", len(src))
print("sections:", src.count('<section class="report"'))
print("verified tags:", src.count('class="tag ok"'))
print("suggestion items:", src.count("<li>") if "<li>" in src else 0)
print("tables:", src.count("<table>"))
print("code-blocks:", src.count('class="code"'))
print("blockquotes:", src.count("<blockquote>"))
print("ext-links:", src.count('target="_blank"'))
print("sources-paras:", src.count('class="sources"'))
print("js-leaks:", src.count("{esc(") + src.count("{stats") + src.count("{chr("))
