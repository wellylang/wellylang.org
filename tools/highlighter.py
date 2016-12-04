#!/usr/bin/env python
"""Syntax-highlights the code blocks within an HTML page as Welly.

Highlights any code within <pre class="prettyprint"> as Welly
except for parts within <samp class="nocode">.
"""

import cgi
import re
import sys

try:
    # Python 3
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    from HTMLParser import HTMLParser


KEYWORDS = {
    'array', 'break', 'box', 'case', 'catch', 'const', 'continue', 'defer',
    'else', 'finally', 'for', 'fulfil', 'fn', 'if', 'in', 'module', 'new',
    'ref', 'return', 'struct', 'switch', 'throw', 'try', 'typeof', 'union',
    'var', 'while',
}

# TODO: Ensure this matches the actual grammar.
SYNTAX_REGEX = re.compile(r'''
      (?P<str>"(?:[^\\\n"]+|\\.)*")
    | (?P<comment>//.*?$ | /\*.*?\*/)
    | (?P<kwd>(?:%s)(?![a-zA-Z_0-9]))
    | (?P<var>[a-zA-Z_][a-zA-Z_0-9]*)
    | (?P<lit>
             \[ | \]
           | '(?:[^\\\n']+|\\.)*'
           | 0x[0-9a-fA-F]+
           | -?[0-9]+ (?: \.[0-9]* (?:[eE][0-9]+)? )?
           | -?\.[0-9]+(?:[eE][0-9]+)?
      )
    | (?P<pun>\S)
    ''' % '|'.join(KEYWORDS), re.VERBOSE | re.DOTALL | re.MULTILINE)

PRETTYPRINT_PRE_REGEX = re.compile(
    r'<pre class=["\']?(?:\w+ )*prettyprint\b[^>]*>(.*?)</pre>', re.DOTALL)

NOCODE_REGEX = re.compile(
    r'<samp class=["\']?(?:\w+ )*nocode\b[^>]*>.*?</samp>', re.DOTALL)

TAG_REGEX = re.compile(r'<[^>]*>')


unescape_html = HTMLParser().unescape


def highlight(text):
    def replace(m):
        for k, v in m.groupdict().items():
            if v:
                return '<span class="%s">%s</span>' % (k, cgi.escape(v))
    return SYNTAX_REGEX.sub(replace, text)


def highlight_html(html):
    return highlight(unescape_html(html))


def process_matches(text, regex, write_match, write_nonmatch, group_number=0):
    """
    For each match for `regex` in `text`, calls `write_nonmatch()` with the
    non-matching text and calls `write_match()` on match group
    `group_number`, and calls `write_nonmatch()` once at the end with any
    trailing non-matching text.
    """
    pos = 0
    for match in regex.finditer(text):
        write_nonmatch(text[pos:match.start(group_number)])
        write_match(match.group(group_number))
        pos = match.end(group_number)
    write_nonmatch(text[pos:])


class SnippetHighlighter(object):
    """An HTML-to-HTML transformation which highlights code snippets."""

    def __init__(self, write):
        self.write = write

    def process_input(self, html):
        """
        Calls `self.write()` on the input HTML. Parts within
        ``<pre class="prettyprint">`` and outside ``<samp class="nocode">``
        are first highlighted with `highlight_html()`.
        """
        process_matches(
            html, PRETTYPRINT_PRE_REGEX, self._process_pp_pre, self.write, 1)

    def _process_pp_pre(self, pp_pre):
        """Process the contents of a ``<pre class="prettyprint">`` tag."""
        process_matches(
            pp_pre, NOCODE_REGEX, self.write, self._process_outside_nocode)

    def _process_outside_nocode(self, html):
        """Process the parts not within ``<samp class="prettyprint">``."""
        process_matches(
            html, TAG_REGEX, self.write, self._write_highlighted_html)

    def _write_highlighted_html(self, nonmatch):
        self.write(highlight_html(nonmatch))


def main():
    html = sys.stdin.read()
    snippet_highlighter = SnippetHighlighter(sys.stdout.write)
    snippet_highlighter.process_input(html)


if __name__ == '__main__':
    main()
