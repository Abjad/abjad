import re


class _LilyParser(object):

    _tokens = (
        ('ARTICULATION',     r'\^|\+|-\||>|.|_'),
        ('BAR',              r'\\bar'),
        ('BEAM_CLOSE',       r']'),
        ('BEAM_OPEN',        r'\['),
        ('CHORD_CLOSE',      r'>'),
        ('CHORD_OPEN',       r'<'),
        ('COMMAND',          r'\\\w+'),
        ('CONTAINER_CLOSE',  r'}'),
        ('CONTAINER_OPEN',   r'{'),
        ('DURATION',         r'[1-9]\d*\.*'),
        ('DYNAMIC',          r'\\(p+|f+|mp|mf|fp|sf|sff|sp|spp|sfz|rfz)$'),
        ('FRACTION',         r'([1-9]\d*)/([1-9]\d*)'),
        ('HAIRPIN_CRESC',    r'\\<'),
        ('HAIRPIN_DECRESC',  r'\\>'),
        ('HAIRPIN_STOP',     r'\\!'),
        ('KEY',              r'\\key'),
        ('KEY_MODE',         r'(major|minor)'),
        ('MARK_DIR_DOWN',    r'_'),
        ('MARK_DIR_NEUTRAL', r'-'),
        ('MARK_DIR_UP',      r'\^'),
        ('OCTAVE',           r"('*|,*)$"),
        ('PITCHCLASS',       r'[a-g][q]?(s*|f*)$'),
        ('REST',             r'[rR]'),
        ('SKIP',             r's'),
        ('SLUR_CLOSE',       r'\)'),
        ('SLUR_OPEN',        r'\('),
        ('STRING',           r'\"[\w\s]+\"'),
        ('TIE',              r'~'),
        ('TIME',             r'\\time'),
        ('TIMES',            r'\\times'),                         
        ('TRILLSPAN_START',  r'\\startTrillSpan'),
        ('TRILLSPAN_STOP',   r'\\stopTrillSpan'),
    )

    _regex = re.compile('|'.join(['(?P<%s>%s)' % (name, rule) for name, rule in _tokens]), re.MULTILINE)

    _whitespace_regex = re.compile("\s*", re.MULTILINE)

    ### OVERRIDES ###

    def __call__(self, lily_string):
        pass

    ### PRIVATE METHODS ###

    def _group_tokens(self, tokens):
        pass

    def _tokenize(self, lily_string):
        pass
        
