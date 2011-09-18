import re
from abjad.exceptions import *
from abjad.tools.iotools._LilyPondToken._LilyPondToken import _LilyPondToken


class _LilyPondTokenizer(object):

    _commands = (
        '\\bar', '\\clef', '\\context', '\\key', '\\new', '\\time', '\\times',
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
     
    _tokens = (
        ('ARTICULATION',     r'(_|-|\^)(\^|\+|-\||>|\.|_)'),
        ('BAR_CHECK',        r'\|'),
        ('BEAM_CLOSE',       r']'),
        ('BEAM_OPEN',        r'\['),
        ('PARALLEL_CLOSE',   r'>>'),
        ('PARALLEL_OPEN',    r'<<'),
        ('CHORD_CLOSE',      r'>'),
        ('CHORD_OPEN',       r'<'),
        ('DOTS',             r'(\.\s*)+'),
        ('EQUALS',           r'='),
        ('HAIRPIN_CRESC',    r'\\<'),
        ('HAIRPIN_DECRESC',  r'\\>'),
        ('HAIRPIN_STOP',     r'\\!'),
        ('COMMAND',          r'\\[a-zA-Z]+'),
        ('CONTAINER_CLOSE',  r'}'),
        ('CONTAINER_OPEN',   r'{'),
        ('DIRECTION',        r'_|-|\^'),
        ('FRACTION',         r'[1-9]\d*/[1-9]\d*'),
        ('INTEGER',          r'[1-9]\d*'),
        ('OCTAVE_DOWN',      r"(,\s*)+"),
        ('OCTAVE_UP',        r"('\s*)+"),
        ('PITCH_CLASS',      r"[a-g][q]?(s*|f*)"),
        ('REST',             r'[rR]'),
        ('SKIP',             r's'),
        ('SLUR_CLOSE',       r'\)'),
        ('SLUR_OPEN',        r'\('),
        ('STRING',           r'\".+\"'),
        ('TIE',              r'~'),
        ('TREMOLO',          r':'),
        ('SYMBOL',           r'\w+'),
    )

    _token_callbacks = {
        'COMMAND':     '_token_callback_command',
        'DOTS':        '_token_callback_strip_whitespace',
        'OCTAVE_DOWN': '_token_callback_strip_whitespace',
        'OCTAVE_UP':   '_token_callback_strip_whitespace',
        'SYMBOL':      '_token_callback_symbol',
    }

    _regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)
        
    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### PRIVATE METHODS ###

    def __call__(self, lily_string):
        tokens = [ ]
        position = 0 
        while position < len(lily_string):
            # match whitespace, in order to skip  
            match = self._whitespace_regex.match(lily_string, position)
            if match:
                position = match.end( )
                if position == len(lily_string):
                    break
            # match token
            match = self._regex.match(lily_string, position)
            if match is None:
                raise UnknownTokenLilyPondParserError(lily_string, position)
            token = _LilyPondToken(match.lastgroup, match.group(match.lastgroup), position)
            # set new position
            position = match.end( )
            # check for callbacks, add to token list
            if token.kind in self._token_callbacks:
                callback = getattr(self, self._token_callbacks[token.kind])
                token = callback(token, lily_string)
            tokens.append(token)
        return tokens

    ### PRIVATE METHODS ###

    def _token_callback_command(self, token, lily_string):
        if token.value in self._commands:
            return token._replace(kind = token.value[1:].upper( ))
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
        return token

