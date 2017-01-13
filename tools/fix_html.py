#!/usr/bin/env python
"""
Convert the HTML to a relatively clean/strict style, with matched tags.
"""

from __future__ import absolute_import

import logging
import os
import re
import sys

from xhtmlify import xhtmlify


logging.basicConfig(level=0)


def use_self_valued_attrs(html):
    '''Replace HTML attributes like ``xyz="xyz"`` with ``xyz``.'''
    def fix_tag(m):
        return re.sub(r'([-_a-zA-Z0-9]+)="\1"', r'\1', m.group())
    return re.sub(r'<[^>]*>', fix_tag, html)


def main():
    args = sys.argv[1:]

    if any(arg.startswith('-') for arg in args):
        sys.exit('usage: %s [HTMLFILE...]' % sys.argv[0])

    if args:
        html_files = args
    else:
        html_files = []
        for basedir, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.html'):
                    html_files.append(os.path.join(basedir, f))


    for f in html_files:
        print(f)
        html = open(f, 'rb').read().decode('utf-8')
        # Fix bad less-than signs which xhtmlify currently rejects.
        html = re.sub(r'(<)([^/!A-Za-z_])', r'&lt;\2', html)
        html = xhtmlify(html)
        # Undo some safe-but-ugly XHTML-isms that we don't currently need.
        html = html.replace(' xmlns="http://www.w3.org/1999/xhtml"', '')
        html = html.replace(' />', '>')
        html = use_self_valued_attrs(html)
        # Prefer named entities.
        html = html.replace('&#x2200;', '&forall;')
        html = html.replace('&#x2203;', '&exist;')
        open(f, 'wb').write(html.encode('utf-8'))


if __name__ == '__main__':
    main()
