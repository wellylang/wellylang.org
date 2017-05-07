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
    'with', # TODO: Remove when it's no longer used.
}

OPERATORS = {
    '!', '!=', '%', '%=', '&', '&&', '&&=', '&=', '*', '**', '**=',
    '*=', '+', '++', '+=', '-', '--', '-=', '/', '/=', '<', '<<', '<<=',
    '<=', '<>', '=', '==', '>', '>=', '>>', '>>=', '>>>', '>>>=', '?', '^',
    '^=', '|', '|=', '||', '||=', '~',
}

ILLEGAL_OPERATORS = {
    '!==', '%==', '&&&', '&&==', '&==', '***', '**==', '*==',
    '+++', '++=', '+==', '---', '--=', '-==', '/==', '<<<', '<<==', '<<>',
    '<==', '<>=', '<>>', '===', '>==', '>>==', '>>>==', '>>>>', '^==', '|==',
    '||==', '|||',
}

SYNTAX_REGEX = re.compile(r'''
      (?P<prompt> >>>> | \.\.\.\.)
    | (?P<comment>//(?:\\\n|.)*?$ | /\*.*?\*/)
    | (?P<kwd>(?:%(keywords)s)(?![a-zA-Z_0-9]))
    | (?P<case>[A-Z_][A-Z_0-9]*(?![a-z]))
    # Actual fields allow newlines but prompts will interfere.
    | (?P<field>\. [\ \t]* [a-zA-Z_][a-zA-Z_0-9]*)
    | (?P<id>[a-zA-Z_][a-zA-Z_0-9]*)
    | (?P<illegal_lit>
          " (?: [^\\\n"]+ | \\.)* (?: \n | \\? \Z )
        | ' (?: [^\\\n']+ | \\.)* (?: \n | \\? \Z )
        | 0x (?! [0-9a-fA-F])
        | \. [0-9]+ [eE] [+-] (?! [0-9])
        | \. [0-9]+ [eE] (?! [0-9+-])
        | [0-9]+ (?: \. [0-9]* )? [eE] [+-] (?! [0-9])
        | [0-9]+ (?: \. [0-9]* )? [eE] (?! [0-9+-])
      )
    | (?P<lit>
          " (?: [^\\\n"]+ | \\.)* "
        | ' (?: [^\\\n']+ | \\.)* '
        | 0x [0-9a-fA-F]+
        | \. [0-9]+ (?:[eE] [+-]? [0-9]+)?
        | [0-9]+ [eE] [+-]? [0-9]+
        | [0-9]+ \. [0-9]* (?:[eE] [+-]? [0-9]+)?
        | [0-9]+
      )
    | (?P<illegal_op>%(illegal_operators)s)
    | (?P<op>%(operators)s)
    | (?P<punc>(?![0-9A-Za-z_\\])[\x21-\x7e])
    | (?P<_escape>\\u[0-9a-fA-F]{0,4}|\\.?)
    | (?P<illegal>\S)
    ''' % dict(
        keywords='|'.join(KEYWORDS),
        operators='|'.join(re.escape(x) for x in OPERATORS),
        illegal_operators='|'.join(re.escape(x) for x in ILLEGAL_OPERATORS),
    ), re.VERBOSE | re.DOTALL | re.MULTILINE)

# TODO: Disallow \b?
ESCAPE_REGEX = re.compile(
    r'''(\\\n)|'''
    r'''(\\[btnfr"'/\\]|\\u[0-9a-fA-F]{4})|'''
    r'''(\\u[0-9a-fA-F]{0,3}|\\)|'''
    r'''[^\\]+''',
    re.DOTALL)

BAD_ESCAPE_REGEX = re.compile(
    r'''\\u[0-9a-fA-F]{0,3}(?![0-9a-fA-F])|\\(?![ubtnfr"'/\\\n])''')

PRETTYPRINT_PRE_REGEX = re.compile(
    r'''<pre class=["\']?(?:\w+ )*prettyprint(?! nocode)\b[^>]*>(.*?)</pre>''',
    re.DOTALL)

NOCODE_REGEX = re.compile(
    r'''(<samp class=["\']?(?:\w+ )*nocode\b[^>]*>.*?</samp>)''',
    re.DOTALL)

TAG_REGEX = re.compile(r'(<[^>]*>)')


unescape_html = HTMLParser().unescape


def highlight(text):
    K = [None]

    def replace_escapes(m):
        cont = m.group(1)
        escape = m.group(2) or m.group(3)
        if escape:
            return '<span class="%s">%s</span>' % (
                'esc' if m.group(2) and K[0] == 'lit' else 'illegal_esc',
                cgi.escape(escape))
        elif cont:
            return '<span class="cont">%s</span>' % (cgi.escape(cont),)
        else:
            return '<span class="%s">%s</span>' % (
                K[0], cgi.escape(m.group()))

    def replace(m):
        for k, v in m.groupdict().items():
            if v:
                if k == 'lit' and BAD_ESCAPE_REGEX.search(v):
                    k = 'illegal_lit'
                K[0] = k
                ret = ESCAPE_REGEX.sub(replace_escapes, v)
                return ret

    return SYNTAX_REGEX.sub(replace, text)


def highlight_html(html):
    return highlight(unescape_html(html))


def process_matches(text, regex, write_match, write_nonmatch):
    """
    For each match for `regex` in `text`, calls `write_nonmatch()` with the
    non-matching text and calls `write_match()` on match group 1, and calls
    `write_nonmatch()` once at the end with any trailing non-matching text.
    """
    pos = 0
    for match in regex.finditer(text):
        write_nonmatch(text[pos:match.start(1)])
        write_match(match.group(1))
        pos = match.end(1)
    write_nonmatch(text[pos:])


# TODO: Only highlight inside <code lang="welly"> or something. Not sure.
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
            html, PRETTYPRINT_PRE_REGEX, self._process_pp_pre, self.write)

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
