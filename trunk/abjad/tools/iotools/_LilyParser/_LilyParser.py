import re


class _LilyParser(object):

    _commands = (
        '\\bar',
        '\\clef',
        '\\key',
        '\\time',
        '\\times',
    )

    _tokens = (
        ('ARTICULATION',     r'(_|-|\^)(\^|\+|-\||>|\.|_)'),
        ('BEAM_CLOSE',       r']'),
        ('BEAM_OPEN',        r'\['),

        ('PARALLEL_CLOSE',   r'>>'),
        ('PARALLEL_OPEN',    r'<<'),
        ('CHORD_CLOSE',      r'>'),
        ('CHORD_OPEN',       r'<'),

        ('HAIRPIN_CRESC',    r'\\<'),
        ('HAIRPIN_DECRESC',  r'\\>'),
        ('HAIRPIN_STOP',     r'\\!'),
        ('DYNAMIC',          r'\\(p+|f+|mp|mf|fp|sf|sff|sp|spp|sfz|rfz)$'),
        ('COMMAND',          r'\\\w+'),

        ('CONTAINER_CLOSE',  r'}'),
        ('CONTAINER_OPEN',   r'{'),
        ('DIRECTION',        r'_|-|\^'),

        ('FRACTION',         r'[1-9]\d*/[1-9]\d*'),
        ('DURATION',         r'[1-9]\d*\.*'),

        ('OCTAVE_DOWN',      r",+"),
        ('OCTAVE_UP',        r"'+"),
        ('PITCH',            r"[a-g][q]?(s*|f*)"),
        ('REST',             r'[rR]'),
        ('SKIP',             r's'),
        ('SLUR_CLOSE',       r'\)'),
        ('SLUR_OPEN',        r'\('),
        ('STRING',           r'\"[\w\s]+\"'),
        ('TIE',              r'~'),
        ('WORD',             r'\w+$'),
    )

    _regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)

    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### OVERRIDES ###

    def __call__(self, lily_string):
        pass

    ### PRIVATE METHODS ###

    def _group(self, tokens):
        pass

    def _tokenize(self, lily_string):
        tokens = [ ]
        position = 0
        while position < len(lily_string):
            # match whitespace
            match = self._whitespace_regex.match(lily_string, position)
            if match:
                position = match.end( )
            # match token
            match = self._regex.match(lily_string, position)
            if match is None:
                raise Exception('Unknown token: ...%s...' % lily_string[position:position + 10])
            position = match.end( )
            value = match.group(match.lastgroup)
            tokens.append((match.lastgroup, value))
            print position, match.lastgroup, value
        return tokens
