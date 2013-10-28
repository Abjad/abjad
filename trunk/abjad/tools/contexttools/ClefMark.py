# -*- encoding: utf-8 -*-
from abjad.tools.contexttools.ContextMark import ContextMark


class ClefMark(ContextMark):
    r'''A clef.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> clef = contexttools.ClefMark('treble')
        >>> attach(clef, staff)
        ClefMark('treble')(Staff{8})
        >>> clef = contexttools.ClefMark('alto')
        >>> attach(clef, staff[1])
        ClefMark('alto')(d'8)
        >>> clef = contexttools.ClefMark('bass')
        >>> attach(clef, staff[2])
        ClefMark('bass')(e'8)
        >>> clef = contexttools.ClefMark('treble^8')
        >>> attach(clef, staff[3])
        ClefMark('treble^8')(f'8)
        >>> clef = contexttools.ClefMark('bass_8')
        >>> attach(clef, staff[4])
        ClefMark('bass_8')(g'8)
        >>> clef = contexttools.ClefMark('tenor')
        >>> attach(clef, staff[5])
        ClefMark('tenor')(a'8)
        >>> clef = contexttools.ClefMark('bass^15')
        >>> attach(clef, staff[6])
        ClefMark('bass^15')(b'8)
        >>> clef = contexttools.ClefMark('percussion')
        >>> attach(clef, staff[7])
        ClefMark('percussion')(c''8)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \clef "treble"
            c'8
            \clef "alto"
            d'8
            \clef "bass"
            e'8
            \clef "treble^8"
            f'8
            \clef "bass_8"
            g'8
            \clef "tenor"
            a'8
            \clef "bass^15"
            b'8
            \clef "percussion"
            c''8
        }

    Clef marks target the staff context by default.
    '''

    ### CLASS VARIABLES ###

    _default_positional_input_arguments = (
        repr('alto'),
        )

    _format_slot = 'opening'

    ### INITIALIZER ###

    def __init__(self, clef_name, target_context=None):
        from abjad.tools.stafftools.Staff import Staff
        target_context = target_context or Staff
        ContextMark.__init__(self, target_context=target_context)
        if isinstance(clef_name, str):
            self._clef_name = clef_name
        elif isinstance(clef_name, type(self)):
            self._clef_name = clef_name.clef_name
        else:
            message = 'can not initialize clef from {}.'.format(clef_name)
            raise TypeError(message)

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies clef.

        ::

            >>> import copy
            >>> clef_1 = contexttools.ClefMark('alto')
            >>> clef_2 = copy.copy(clef_1)

        ::

            >>> clef_1, clef_2
            (ClefMark('alto'), ClefMark('alto'))

        ::

            >>> clef_1 == clef_2
            True

        ::

            >>> clef_1 is clef_2
            False

        Returns new clef.
        '''
        return type(self)(
            self.clef_name, 
            target_context=self.target_context,
            )

    def __eq__(self, arg):
        r'''True when clef name of `arg` equal clef name of clef.
        Otherwise false.

        ::

            >>> clef_1 = contexttools.ClefMark('treble')
            >>> clef_2 = contexttools.ClefMark('alto')

        ::

            >>> clef_1 == clef_1
            True
            >>> clef_1 == clef_2
            False
            >>> clef_2 == clef_1
            False
            >>> clef_2 == clef_2
            True

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            return self._clef_name == arg._clef_name
        return False

    def __ne__(self, arg):
        r'''True when clef of `arg` does not equal clef name of clef.
        False otherwise.

        ::

            >>> clef_1 = contexttools.ClefMark('treble')
            >>> clef_2 = contexttools.ClefMark('alto')

        ::

            >>> clef_1 != clef_1
            False
            >>> clef_1 != clef_2
            True
            >>> clef_2 != clef_1
            True
            >>> clef_2 != clef_2
            False

        Returns boolean.
        '''
        superclass = super(ClefMark, self)
        return superclass.__ne__(arg)

    def __repr__(self):
        r'''Interpreter representation of clef.

        ::

            >>> clef = contexttools.ClefMark('treble')
            >>> clef
            ClefMark('treble')

        Returns string.
        '''
        superclass = super(ClefMark, self)
        return superclass.__repr__()

    ### PRIVATE PROPERTIES ###

    _clef_name_to_middle_c_position = {
        'treble': -6,
        'alto': 0,
        'tenor': 2,
        'bass': 6,
        'french': -8,
        'soprano': -4,
        'mezzosoprano': -2,
        'baritone': 4,
        'varbaritone': 4,
        'percussion': 0,
        'tab': 0
    }

    @property
    def _contents_repr_string(self):
        return repr(self._clef_name)

    ### PUBLIC METHODS ###

    @classmethod
    def list_clef_names(cls):
        r'''Lists clef names.

        ::

            >>> for name in contexttools.ClefMark.list_clef_names():
            ...     name
            ...
            'alto'
            'baritone'
            'bass'
            'french'
            'mezzosoprano'
            'percussion'
            'soprano'
            'tab'
            'tenor'
            'treble'
            'varbaritone'

        Returns list of strings.
        '''
        return list(sorted(cls._clef_name_to_middle_c_position))

    ### PUBLIC PROPERTIES ###

    @apply
    def clef_name():
        def fget(self):
            r'''Gets and sets clef name.

            ::

                >>> clef = contexttools.ClefMark('treble')
                >>> clef.clef_name
                'treble'

            ::

                >>> clef.clef_name = 'alto'
                >>> clef.clef_name
                'alto'

            Returns string.
            '''
            return self._clef_name
        def fset(self, clef_name):
            assert isinstance(clef_name, str)
            self._clef_name = clef_name
        return property(**locals())

    @property
    def lilypond_format(self):
        r'''LilyPond format of clef.

        ::

            >>> clef = contexttools.ClefMark('treble')
            >>> clef.lilypond_format
            '\\clef "treble"'

        Returns string.
        '''
        return r'\clef "%s"' % self._clef_name

    @property
    def middle_c_position(self):
        r'''Middle C position of clef.

        ::

            >>> clef = contexttools.ClefMark('treble')
            >>> clef.middle_c_position
            -6

        Returns integer number of stafflines.
        '''
        alteration = 0
        if '_' in self._clef_name:
            base_name, part, suffix = self._clef_name.partition('_')
            if suffix == '8':
                alteration = 7
            elif suffix == '15':
                alteration = 13
            else:
                message = "Bad clef alteration suffix: {!r}"
                message = message.format(suffix)
                raise Exception(message)
        elif '^' in self._clef_name:
            base_name, part, suffix = self._clef_name.partition('^')
            if suffix == '8':
                alteration = -7
            elif suffix == '15':
                alteration = -13
            else:
                message = "Bad clef alteration suffix: {!r}"
                message = message.format(suffix)
                raise Exception(message)
        else:
            base_name = self._clef_name
        return self._clef_name_to_middle_c_position[base_name] + alteration

    @property
    def storage_format(self):
        r'''Storage format of clef.

        ::

            >>> print clef.storage_format
            contexttools.ClefMark(
                'treble',
                target_context=stafftools.Staff
                )

        Returns string.
        '''
        superclass = super(ClefMark, self)
        return superclass.storage_format
