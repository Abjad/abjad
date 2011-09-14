import re


class _LilyParser(object):

    tokens = {
        'ARTICULATION':     r'\\()',
        'BAR':              r'\\bar',
        'BEAM_CLOSE':       r']',
        'BEAM_OPEN':        r'\[',
        'CHORD_CLOSE':      r'>',
        'CHORD_OPEN':       r'<',
        'COMMAND':          r'\\\w+',
        'CONTAINER_CLOSE':  r'}',
        'CONTAINER_OPEN':   r'{',
        'DURATION':         r'[1-9]\d*\.*',
        'FRACTION':         r'([1-9]\d*)/([1-9]\d*)',
        'KEY':              r'\\key',
        'KEY_MODE':         r'(major|minor)',
        'MARK_DIR_DOWN':    r'_',
        'MARK_DIR_NEUTRAL': r'-',
        'MARK_DIR_UP':      r'\^',
        'OCTAVE':           r"('*|,*)$",
        'PITCHCLASS':       r'[a-g][q]?(s*|f*)$',
        'REST':             r'[rR]',
        'SKIP':             r's',
        'SLUR_CLOSE':       r'\)',
        'SLUR_OPEN':        r'\(',
        'STRING':           r'\"[\w\s]+\"',
        'TIE':              r'~',
        'TIME':             r'\\time',
        'TIMES':            r'\\times',                         
    }

    ### OVERRIDES ###

    def __call__(self, lily_string):
        pass

    ### PRIVATE METHODS ###

    def _tokenize(self, lily_string):
        pass

    def _group_tokens(self, tokens):
        pass
