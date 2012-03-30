"""This library parses dotlang files.

Lifted from Bedrock.
"""

import codecs
import logging
import os

import settings


# Don't even THINK this is thread-safe.
CACHE = {}


def parse(path):
    """Parse a dotlang file and return a dict of translations."""
    trans = {}

    if not os.path.exists(path):
        return trans

    with codecs.open(path, 'r', 'utf-8') as lines:
        source = None

        for line in lines:
            line = line.strip()
            if line != '':
                if line[0] == ';':
                    source = line
                elif source:
                    trans[source[1:]] = line

    return trans


def load(lang):
    """Load the dotlang files for the specific lang and cache them in
    django."""

    path = os.path.join(settings.ROOT, 'locale', '%s.lang' % lang)
    trans = parse(path)

    CACHE['trans-%s' % lang] = trans
    return trans


def translate(lang, text, warn=True):
    """Translate a piece of text, loading the language's dotlang files
    if they aren't cached"""

    key = 'trans-%s' % lang
    trans = CACHE.get(key)

    if not trans:
        trans = load(lang)

    try:
        translated = trans[text]
    except KeyError:
        if warn:
            logging.warning('Unknown text "%s" for language %s' % (text, lang))
        translated = text
    return translated
