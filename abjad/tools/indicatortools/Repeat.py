# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Repeat(AbjadValueObject):
    r'''A repeat indicator.

    ..  container:: example

        ::

            >>> container = Container("c'4 d'4 e'4 f'4")
            >>> repeat = indicatortools.Repeat()
            >>> attach(repeat, container)
            >>> show(container)  # doctest: +SKIP

        ..  doctest::

            >>> print(format(container))
            \repeat volta 2
            {
                c'4
                d'4
                e'4
                f'4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_repeat_count',
        '_repeat_type',
        )

    _format_leaf_children = False

    _format_slot = 'before'

    ### INITIALIZER ###

    def __init__(self, repeat_count=2, repeat_type='volta'):
        repeat_count = int(repeat_count)
        assert 1 < repeat_count
        self._repeat_count = repeat_count
        assert repeat_type in ('volta', 'unfold')
        self._repeat_type = repeat_type

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of repeat.

        ..  container:: example

            ::

                >>> str(indicatortools.Repeat())
                '\\repeat volta 2'

        Returns string.
        '''
        return r'\repeat {} {}'.format(
            self.repeat_type,
            self.repeat_count,
            )

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.before.commands.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def repeat_count(self):
        r'''Gets repeat count of repeat.

        ..  container:: example

            ::

                >>> repeat = indicatortools.Repeat()
                >>> repeat.repeat_count
                2

        Returns integer.
        '''
        return self._repeat_count

    @property
    def repeat_type(self):
        r'''Gets repeat type of repeat.

        ..  container:: example

            ::

                >>> repeat = indicatortools.Repeat()
                >>> repeat.repeat_type
                'volta'

        Returns string.
        '''
        return self._repeat_type