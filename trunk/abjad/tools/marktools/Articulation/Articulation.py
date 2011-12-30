from abjad.tools.componenttools._Component import _Component
from abjad.tools.marktools.Mark import Mark


class Articulation(Mark):
    '''Abjad model of musical articulation::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.Articulation('staccato')(note)
        Articulation('staccato')(c'4)

    ::

        abjad> f(note)
        c'4 -\staccato

    Articulations implement ``__slots__``.
    '''

    __slots__ = ('_string', '_direction', '_format_slot')

    def __init__(self, *args):
        assert len(args) in range(3)
        Mark.__init__(self)
        if 2 <= len(args):
            assert isinstance(args[0], (str, type(None)))
            assert isinstance(args[1], (str, type(None)))
            string, direction = args
        elif len(args) == 1:
            assert isinstance(args[0], (str, type(None)))
            if args[0]:
                splits = args[0].split('\\')
                assert len(splits) in (1, 2)
                if len(splits) == 1:
                    string, direction = args[0], None
                elif len(splits) == 2:
                    string = splits[1]
                    if splits[0]:
                        direction = splits[0]
                    else:
                        direction = None
            else:
                string, direction = None, None
        else:
            string, direction = None, None

        if direction in ('^', 'up'):
            direction = '^'
        elif direction in ('_', 'down'):
            direction = '_'
        elif direction in ('-', 'default'):
            direction = '-'
        elif direction is None:
            direction = None
        else:
            raise ValueError('can not set articulation direction.')

        object.__setattr__(self, '_string', string)
        object.__setattr__(self, '_direction', direction)
        self._format_slot = 'right'

    ### OVERLOADS ###

    def __copy__(self, *args):
        return type(self)(self.name, self.direction_string)

    __deepcopy__ = __copy__

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if expr.name == self.name:
                if self.direction_string == expr.direction_string:
                    return True
        return False

    def __str__(self):
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction_string is None:
                direction_string = '-'
            else:
                direction_string = self.direction_string
            return '%s\%s' % (direction_string, string)
        else:
            return ''

    ### PRIVATE ATTRIBUTES ###

    # this causes unnecessary coupling to changeable lilypond codebase and is discouraged
    _articulations_supported = ('accent', 'marcato',
        'staccatissimo',        'espressivo'
        'staccato',             'tenuto'                 'portato'
        'upbow',                  'downbow'                'flageolet'
        'thumb',                  'lheel'                  'rheel'
        'ltoe',                   'rtoe'                   'open'
        'stopped',                'turn'                   'reverseturn'
        'trill',                  'prall'                  'mordent'
        'prallprall'            'prallmordent',        'upprall',
        'downprall',            'upmordent',           'downmordent',
        'pralldown',            'prallup',             'lineprall',
        'signumcongruentiae', 'shortfermata',        'fermata',
        'longfermata',          'verylongfermata',   'segno',
        'coda',                   'varcoda',
        '^', '+', '-', '|', '>', '.', '_',
        )

    # this causes unnecessary coupling to changeable lilypond codebase and is discouraged
    _shortcut_to_word = {
            '^':'marcato', '+':'stopped', '-':'tenuto', '|':'staccatissimo',
            '>':'accent', '.':'staccato', '_':'portato' }

    @property
    def _contents_repr_string(self):
        if self.direction_string is not None:
            return '%r, %r' % (self.name, self.direction_string)
        else:
            return repr(self.name)

    ### PUBLIC ATTRIBUTES ###

    @apply
    def direction_string():
        def fget(self):
            '''Get direction string of articulation::

                abjad> articulation = marktools.Articulation('staccato')
                abjad> articulation.direction_string is None
                True

            Set direction string of articulation::

                abjad> articulation.direction_string = '^'
                abjad> articulation.direction_string
                '^'

            Set string.
            '''
            return self._direction
        def fset(self, direction_string):
            assert isinstance(direction_string, (str, type(None)))
            self._direction = direction_string
        return property(**locals())

    @property
    def format(self):
        '''Read-only LilyPond format string of articulation::

            abjad> articulation = marktools.Articulation('marcato', 'up')
            abjad> articulation.format
            '^\\marcato'

        Return string.
        '''
        return str(self)

    @apply
    def name():
        def fget(self):
            '''Get name of articulation::

                abjad> articulation = marktools.Articulation('staccato', 'up')
                abjad> articulation.name
                'staccato'

            Set name of articulation::

                abjad> articulation.name = 'marcato'
                abjad> articulation.name
                'marcato'

            Set string.
            '''
            return self._string
        def fset(self, name):
            assert isinstance(name, str)
            self._string = name
        return property(**locals())
