import re


class _LilyPondParser(object):

    _callbacks = {
        'COMMAND': '_callback_command_token',
        'OBJ': '_callback_obj_token',
    }

    _commands = {
        'BAR': ['STRING'],
        'CLEF': ['SYMBOL'],
        'CONTEXT': ['CONTEXT_TYPE', 'EQUALS', 'STRING'],
        'KEY': ['PITCHCLASS', 'SYMBOL'],
        'NEW': ['CONTEXT_TYPE'],
        'TEMPO': ['UNSIGNED_INT', 'EQUALS', 'UNSIGNED_INT'],
        'TIME': ['FRACTION'],
        'TIMES': ['FRACTION'],
    }

    _context_types = (
        'Score',
        'Staff',
        'Voice',
    )

    _tokens = (
        ('ARTICULATION',     r'(_|-|\^)(\^|\+|-\||>|\.|_)'),
        ('BEAM_CLOSE',       r']'),
        ('BEAM_OPEN',        r'\['),

        ('PARALLEL_CLOSE',   r'>>'),
        ('PARALLEL_OPEN',    r'<<'),
        ('CHORD_CLOSE',      r'>'),
        ('CHORD_OPEN',       r'<'),

        ('EQUALS',           r'='),

        ('HAIRPIN_CRESC',    r'\\<'),
        ('HAIRPIN_DECRESC',  r'\\>'),
        ('HAIRPIN_STOP',     r'\\!'),
        ('DYNAMIC',          r'\\(p+|f+|mp|mf|fp|sf|sff|sp|spp|sfz|rfz)$'),
        ('COMMAND',          r'\\\w+'),

        ('CONTAINER_CLOSE',  r'}'),
        ('CONTAINER_OPEN',   r'{'),
        ('DIRECTION',        r'_|-|\^'),

        ('FRACTION',         r'[1-9]\d*/[1-9]\d*'),
        ('UNSIGNED_INT',     r'[1-9]\d*'),
        ('DOTS',             r'\.+'),

        ('OCTAVE_DOWN',      r",+"),
        ('OCTAVE_UP',        r"'+"),
        ('PITCHCLASS',       r"[a-g][q]?(s*|f*)"),
        ('REST',             r'[rR]'),
        ('SKIP',             r's'),
        ('SLUR_CLOSE',       r'\)'),
        ('SLUR_OPEN',        r'\('),
        ('STRING',           r'\".+\"'),
        ('TIE',              r'~'),

        ('SYMBOL',           r'\w+$'),
        ('OBJ',              r'[A-Z][a-zA-Z]+'),
    )

    _regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)

    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### OVERRIDES ###

    def __call__(self, lily_string):
        pass

    ### PRIVATE METHODS ###

    def _group(self, tokens):
        pass

    def _callback_command_token(self, token, value):
        if value in [
            '\\bar',
            '\\clef',
            '\\context',
            '\\key',
            '\\new',
            '\\time',
            '\\times']:
            token = value[1:].upper( )
        return token, value

    def _callback_obj_token(self, token, value):
        if value in [
            'Score',
            'Staff',
            'Voice']:
            token = 'CONTEXT_TYPE'
        return token, value

    def _tokenize(self, lily_string):
        tokens = [ ]
        position = 0
        while position < len(lily_string):
            # match whitespace
            match = self._whitespace_regex.match(lily_string, position)
            if match:
                position = match.end( )
                if position == len(lily_string):
                    break
            # match token
            match = self._regex.match(lily_string, position)
            if match is None:
                raise Exception('Unknown token at character %d: %s' % \
                    (position, lily_string[position:position + 10]))
            position = match.end( )
            token = match.lastgroup
            value = match.group(match.lastgroup)
            # check for callbacks, add to token list
            if token in self._callbacks:
                callback = getattr(self, self._callbacks[token])
                token, value = callback(token, value)
                tokens.append(callback(token, value))
            else:
                tokens.append((token, value))
        return tokens
