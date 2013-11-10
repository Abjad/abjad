# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.marktools.Mark import Mark


class Articulation(Mark):
    r'''An articulation.

    ..  container:: example

        Initializes from name:

        ::

            >>> Articulation('staccato')
            Articulation('staccato')

    ..  container:: example

        Initializes from abbreviation:

        ::

            >>> Articulation('.')
            Articulation('.')

    ..  container:: example

        Initializes from other articulation:

        ::

            >>> articulation = Articulation('staccato')
            >>> Articulation(articulation)
            Articulation('staccato')

    ..  container:: example

        Initializes with direction:

        ::

            >>> Articulation('staccato', Up)
            Articulation('staccato', Up)

    .. container:: example

        Use `attach()` to attach articulations to notes, rests or chords:

        ::

            >>> note = Note("c'4")
            >>> articulation = Articulation('staccato')
            >>> attach(articulation, note)
            >>> show(note) # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_string', 
        '_direction', 
        '_format_slot',
        )

    ### INITIALIZER ###

    def __init__(self, *args):
        from abjad.tools import datastructuretools
        assert len(args) in range(3), repr(args)
        if 2 <= len(args):
            assert isinstance(args[0], (str, type(None))), repr(args[0])
            assert isinstance(args[1], 
                (str, type(None), datastructuretools.OrdinalConstant)), \
                repr(args[1])
            string, direction = args
        elif len(args) == 1 and isinstance(args[0], type(self)):
            string = args[0].name
            direction = args[0].direction
        elif len(args) == 1:
            assert isinstance(args[0], 
                (str, type(None), datastructuretools.OrdinalConstant)), \
                repr(args[0])
            if args[0]:
                splits = args[0].split('\\')
                assert len(splits) in (1, 2), repr(splits)
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
        Mark.__init__(self)
        self._string = string
        self.direction = direction
        self._format_slot = 'right'

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies articulation.

        Returns new articulation.
        '''
        return type(self)(self.name, self.direction)

    def __eq__(self, expr):
        r'''True when `expr` equals name and direction of articulation.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if expr.name == self.name:
                if self.direction == expr.direction:
                    return True
        return False

    def __str__(self):
        r'''String representation of articulation.

        Returns string.
        '''
        if self.name:
            string = self._shortcut_to_word.get(self.name)
            if not string:
                string = self.name
            if self.direction is None:
                direction = '-'
            else:
                direction = \
                    stringtools.arg_to_tridirectional_lilypond_symbol(
                    self.direction)
            return '%s\%s' % (direction, string)
        else:
            return ''

    ### PRIVATE PROPERTIES ###

    # this causes unnecessary coupling to changeable lilypond codebase 
    # and is discouraged
    _articulations_supported = (
        'accent', 
        'marcato',
        'staccatissimo',        
        'espressivo'
        'staccato',             
        'tenuto'                 
        'portato'
        'upbow',                  
        'downbow'                
        'flageolet'
        'thumb',                  
        'lheel'                  
        'rheel'
        'ltoe',                   
        'rtoe'                   
        'open'
        'stopped',                
        'turn'                   
        'reverseturn'
        'trill',                  
        'prall'                  
        'mordent'
        'prallprall'            
        'prallmordent',        
        'upprall',
        'downprall',            
        'upmordent',           
        'downmordent',
        'pralldown',            
        'prallup',             
        'lineprall',
        'signumcongruentiae', 
        'shortfermata',        
        'fermata',
        'longfermata',          
        'verylongfermata',   
        'segno',
        'coda',                   
        'varcoda',
        '^', 
        '+', 
        '-', 
        '|', 
        '>', 
        '.', 
        '_',
        )

    # this causes unnecessary coupling to changeable lilypond codebase 
    # and is discouraged
    _shortcut_to_word = {
        '^':'marcato', 
        '+':'stopped', 
        '-':'tenuto', 
        '|':'staccatissimo',
        '>':'accent', 
        '.':'staccato', 
        '_':'portato',
        }

    @property
    def _contents_repr_string(self):
        if self.direction is not None:
            return '{!r}, {!r}'.format(self.name, self.direction)
        else:
            return repr(self.name)

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @apply
    def direction():
        def fget(self):
            r'''Gets and sets direction of articulation.

            ..  container:: example

                Example score:

                ::

                    >>> note = Note("c'4")
                    >>> articulation = Articulation('staccato', Down)
                    >>> attach(articulation, note)
                    >>> show(note) # doctest: +SKIP

            ..  container:: example

                Gets property:

                ::

                    >>> articulation.direction
                    Down

            ..  container:: example

                Sets property:

                ::

                    >>> articulation.direction = Up
                    >>> show(note) # doctest: +SKIP

            Returns string.
            '''
            return self._direction
        def fset(self, arg):
            arg = stringtools.arg_to_tridirectional_ordinal_constant(arg)
            self._direction = arg
        return property(**locals())

    @apply
    def name():
        def fget(self):
            r'''Gets and sets name of articulation.

            ..  container:: example

                Gets property:

                ::

                    >>> articulation = Articulation('staccato')
                    >>> articulation.name
                    'staccato'

            ..  container:: example

                Sets property:

                ::

                    >>> articulation.name = 'marcato'
                    >>> articulation.name
                    'marcato'

            Returns string.
            '''
            return self._string
        def fset(self, name):
            assert isinstance(name, str), repr(name)
            self._string = name
        return property(**locals())
