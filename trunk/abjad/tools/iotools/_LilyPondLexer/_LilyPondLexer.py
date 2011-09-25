import re
from abjad.exceptions import *
from abjad.tools.iotools._LilyPondToken._LilyPondToken import _LilyPondToken


class _LilyPondLexer(object):

    _articulations = (
        '\\accent', '\\accentus', '\\circulus', '\\coda', '\\downbow', '\\downmordent',
        '\\downprall', '\\espressivo', '\\fermata', '\\flageolet', '\\halfopen',
        '\\ictus', '\\lheel', '\\lineprall', '\\longfermata', '\\ltoe', '\\marcato',
        '\\mordent', '\\open', '\\portato', '\\prall', '\\pralldown', '\\prallmordent',
        '\\prallprall', '\\prallup', '\\reverseturn', '\\rheel', '\\rtoe', '\\segno',
        '\\semicirculus', '\\shortfermata', '\\signumcongruentiae', '\\snappizzicato',
        '\\staccatissimo', '\\staccato', '\\stopped', '\\tenuto', '\\thumb', '\\trill'
        '\\turn', '\\upbow', '\\upmordent', '\\upprall', '\\varcoda', '\\verylongfermata',
    )

    _blocks = (
        '\\book', '\\header', '\\layout', '\\midi', '\\score',
    )

    _commands = (
        '\\bar', '\\clef', '\\key', '\\markup', '\\tempo', '\\time', '\\times',
    )

    _context_types = (
        'PianoStaff', 'Score', 'Staff', 'Voice',
    )

    _durations = (
        '\\breve', '\\longa', '\\maxima',
        '1', '2', '4', '8', '16', '32', '64', '128',
    )

    _dynamics = (
        '\\mp', '\\mf',
        '\\fp', '\\sf', '\\sff', '\\sp', '\\spp', '\\sfz', '\\rfz',
        '\\p', '\\pp', '\\ppp', '\\pppp', '\\ppppp',
        '\\f', '\\ff', '\\fff', '\\ffff', '\\fffff'
    )
     
    _keywords = (
        '\\context', '\\include', '\\new', '\\once', '\\override',
        '\\version', '\\with',
    )

    _tokens = (
        ('ARTICULATION_SHORTCUT', r'(_|-|\^)\s*(\^|\+|-\||>|\.|_)'),
        ('BAR_CHECK',             r'\|'),
        ('BEAM_CLOSE',            r']'),
        ('BEAM_OPEN',             r'\['),
        ('PARALLEL_CLOSE',        r'>>'),
        ('PARALLEL_OPEN',         r'<<'),
        ('CHORD_CLOSE',           r'>'),
        ('CHORD_OPEN',            r'<'),
        ('DOTS',                  r'(\.\s*)+'),
        ('EQUALS',                r'='),
        ('HAIRPIN_CRESC',         r'\\<'),
        ('HAIRPIN_DECRESC',       r'\\>'),
        ('HAIRPIN_STOP',          r'\\!'),
        ('COMMAND',               r'\\[a-zA-Z]+'),
        ('CONTAINER_CLOSE',       r'}'),
        ('CONTAINER_OPEN',        r'{'),
        ('DIRECTION',             r'_|-|\^'),
        ('FRACTION',              r'[1-9]\d*/[1-9]\d*'),
        ('INTEGER',               r'[1-9]\d*'),
        ('OCTAVE_DOWN',           r"(,\s*)+"),
        ('OCTAVE_UP',             r"('\s*)+"),
        ('SYMBOL',                r'\w+'),
        ('REST',                  r'[rR]'),
        ('SKIP',                  r's'),
        ('SLUR_CLOSE',            r'\)'),
        ('SLUR_OPEN',             r'\('),
        ('STRING',                r'\".+\"'),
        ('TIE',                   r'~'),
        ('TREMOLO',               r':'),
    )

    _token_callbacks = {
        'ARTICULATION_SHORTCUT': '_token_callback_strip_whitespace',
        'COMMAND':               '_token_callback_command',
        'DOTS':                  '_token_callback_strip_whitespace',
        'OCTAVE_DOWN':           '_token_callback_strip_whitespace',
        'OCTAVE_UP':             '_token_callback_strip_whitespace',
        'SYMBOL':                '_token_callback_symbol',
    }

    _token_regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)
        
    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### OVERRIDES ###

    def __call__(self, lily_string):
        tokens = [ ]
        lines = lily_string.split('\n')
        for line_number, line in enumerate(lines):
            column = 0
            while column < len(line):
                match = self._whitespace_regex.match(line, column)
                if match:
                    column = match.end( )
                if column == len(line):
                    break
                match = self._token_regex.match(line, column)
                if match is None:
                    raise UnknownTokenLilyPondParserError(lily_string, line_number, column)
                token = _LilyPondToken(
                    kind = match.lastgroup,
                    value = match.group(match.lastgroup),
                    line = line_number,
                    column = column)
                column = match.end( )
                if token.kind in self._token_callbacks:
                    callback = getattr(self, self._token_callbacks[token.kind])
                    token = callback(token, lily_string)
                tokens.append(token)
        return tokens

    ### PRIVATE METHODS ###

    def _token_callback_command(self, token, lily_string):
        if token.value in self._commands:
            return token._replace(kind = token.value[1:].upper( ))
        elif token.value in self._keywords:
            return token._replace(kind = 'KEYWORD')
        elif token.value in self._articulations:
            return token._replace(kind = 'ARTICULATION')
        elif token.value in ['\\longa', '\\breve', '\\maxima']:
            return token._replace(kind = 'DURATION')
        elif token.value in self._dynamics:
            return token._replace(kind = 'DYNAMIC')
        return token
            
    def _token_callback_strip_whitespace(self, token, lily_string):
        new_value = ''
        for c in token.value:
            if not c.isspace( ):   
                new_value += c
        return token._replace(value = new_value)
            
    def _token_callback_symbol(self, token, lily_string):
        if token.value in self._context_types:
            return token._replace(kind = 'CONTEXT_TYPE')
        else:
            match = re.match(r"[a-g][q]?(s*|f*)", token.value)
            if match is not None and match.end( ) == len(token.value):
                token = token._replace(kind = 'PITCH_CLASS')
        return token
