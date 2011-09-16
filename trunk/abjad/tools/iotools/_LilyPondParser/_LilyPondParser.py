import re


class _LilyPondParser(object):

    _commands = (
        '\\bar', '\\clef', '\\context', '\\key', '\\new', '\\time', '\\times'
    )

    _commands_arguments = {
        'BAR': ['STRING'],
        'CLEF': ['SYMBOL'],
        'CONTEXT': ['CONTEXT_TYPE', 'EQUALS', 'STRING'],
        'KEY': ['PITCHCLASS', 'SYMBOL'],
        'NEW': ['CONTEXT_TYPE'],
        'TEMPO': ['INTEGER', 'EQUALS', 'INTEGER'],
        'TIME': ['FRACTION'],
        'TIMES': ['FRACTION'],
    }

    _context_types = (
        'Score',
        'Staff',
        'Voice',
    )

    _dynamics = (
        '\\mp', '\\mf',
        '\\fp', '\\sf', '\\sff', '\\sp', '\\spp', '\\sfz', '\\rfz',
        '\\p', '\\pp', '\\ppp', '\\pppp', '\\ppppp',
        '\\f', '\\ff', '\\fff', '\\ffff', '\\fffff'
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
        ('COMMAND',          r'\\[a-zA-Z]+'),

        ('CONTAINER_CLOSE',  r'}'),
        ('CONTAINER_OPEN',   r'{'),
        ('DIRECTION',        r'_|-|\^'),

        ('FRACTION',         r'[1-9]\d*/[1-9]\d*'),
        ('INTEGER',          r'[1-9]\d*'),
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

        ('SYMBOL',           r'\w+'),
    )

    _token_callbacks = {
        'COMMAND': '_callback_command_token',
        'SYMBOL': '_callback_symbol_token',
    }

    _regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)

    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### OVERRIDES ###

    def __call__(self, lily_string):
        pass

    ### PRIVATE METHODS ###

    def _group(self, tokens):
        pass

    def _callback_command_token(self, token, value):
        if value in self._commands:
            token = value[1:].upper( )
        elif value in self._dynamics:
            token = 'DYNAMIC'
        return token, value

    def _callback_symbol_token(self, token, value):
        if value in [
            'Score',
            'Staff',
            'Voice']:
            token = 'CONTEXT_TYPE'
        return token, value

    def _tokenize(self, lily_string):
        '''Scan through `lily_string`, matching tokens and discarding whitespace.
        Certain tokens have callbacks for finer-grain parsing.
        '''
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
            if token in self._token_callbacks:
                callback = getattr(self, self._token_callbacks[token])
                token, value = callback(token, value)
                tokens.append(callback(token, value))
            else:
                tokens.append((token, value))
        return tokens
