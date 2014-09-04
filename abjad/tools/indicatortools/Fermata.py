# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class Fermata(AbjadObject):
    r'''A fermata.

    ..  container:: example

        Fermata:

        ::

            >>> note = Note("c'4")
            >>> fermata = indicatortools.Fermata()
            >>> attach(fermata, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 \fermata

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_command',
        )


    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, command='fermata'):
        assert command in (
            'shortfermata',
            'fermata',
            'longfermata',
            'verylongfermata',
            ), repr(fermata)
        self._command = command

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies fermata.

        ..  container:: example

            ::

                >>> import copy
                >>> fermata_1 = indicatortools.Fermata(command='shortfermata')
                >>> fermata_2 = copy.copy(fermata_1)

            ::

                >>> str(fermata_1) == str(fermata_2)
                True

            ::

                >>> fermata_1 == fermata_2
                True

            ::

                >>> fermata_1 is fermata_2
                False

        Returns new fermata.
        '''
        return type(self)(command=self.command)

    def __eq__(self, expr):
        r'''Is true when `expr` is a fermata with command
        equal to that of this fermata. Otherwise false.

        ..  container:: example

            ::

                >>> fermata_1 = indicatortools.Fermata()
                >>> fermata_2 = indicatortools.Fermata()
                >>> fermata_3 = indicatortools.Fermata(command='shortfermata')

            ::

                >>> fermata_1 == fermata_1
                True
                >>> fermata_1 == fermata_2
                True
                >>> fermata_1 == fermata_3
                False

            ::

                >>> fermata_2 == fermata_1
                True
                >>> fermata_2 == fermata_2
                True
                >>> fermata_2 == fermata_3
                False

            ::

                >>> fermata_3 == fermata_1
                False
                >>> fermata_3 == fermata_2
                False
                >>> fermata_3 == fermata_3
                True

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.command == expr.command:
                return True
        return False

    def __hash__(self):
        r'''Hashes fermata.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Fermata, self).__hash__()

    def __str__(self):
        r'''Gets string representation of fermata.

        ..  container:: example

            ::

                >>> str(indicatortools.Fermata())
                '\\fermata'

        Returns string.
        '''
        return r'\{}'.format(self.command)

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.articulations.append(str(self))
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def command(self):
        r'''Gets command of fermata.

        ..  container:: example

            ::

                >>> fermata = indicatortools.Fermata()
                >>> fermata.command
                'fermata'

        Returns string.
        '''
        return self._command