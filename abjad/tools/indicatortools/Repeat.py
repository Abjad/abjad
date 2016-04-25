# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class Repeat(AbjadValueObject):
    r'''A repeat indicator.

    ..  container:: example

        **Example 1.** Volta repeat:

        ::

            >>> container = Container("c'4 d'4 e'4 f'4")
            >>> repeat = indicatortools.Repeat()
            >>> attach(repeat, container)
            >>> staff = Staff([container])
            >>> score = Score([staff])
            >>> show(score)  # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \repeat volta 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    ..  container:: example

        **Example 2.** Unfold repeat:

        ::

            >>> container = Container("c'4 d'4 e'4 f'4")
            >>> repeat = indicatortools.Repeat(repeat_type='unfold')
            >>> attach(repeat, container)
            >>> staff = Staff([container])
            >>> score = Score([staff])
            >>> show(score)  # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    \repeat unfold 2
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                    }
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_repeat_count',
        '_repeat_type',
        )

    _format_leaf_children = False

    _format_slot = 'before'

    ### INITIALIZER ###

    def __init__(self, repeat_count=2, repeat_type='volta'):
        from abjad.tools import scoretools
        # TODO: make score-scoped
        #self._default_scope = scoretools.Score
        self._default_scope = None
        repeat_count = int(repeat_count)
        assert 1 < repeat_count
        self._repeat_count = repeat_count
        assert repeat_type in ('volta', 'unfold')
        self._repeat_type = repeat_type

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of repeat.

        ..  container:: example

            **Example 1.** Volta repeat:

            ::

                >>> str(indicatortools.Repeat())
                '\\repeat volta 2'

        ..  container:: example

            **Example 2.** Unfold repeat:

            ::

                >>> str(indicatortools.Repeat(repeat_type='unfold'))
                '\\repeat unfold 2'

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
    def default_scope(self):
        r'''Gets default scope of repeat.

        ..  container:: example

            **Example 1.** Volta repeat:

            ::

                >>> repeat = indicatortools.Repeat()
                >>> repeat.default_scope is None
                True

        ..  container:: example

            **Example 2.** Unfold repeat:

            ::

                >>> repeat = indicatortools.Repeat(repeat_type='unfold')
                >>> repeat.default_scope is None
                True

        ..  todo:: Make repeats score-scoped.

        Returns none (but should return score).
        '''
        return self._default_scope

    @property
    def repeat_count(self):
        r'''Gets repeat count of repeat.

        ..  container:: example

            **Example 1.** Volta repeat:

            ::

                >>> repeat = indicatortools.Repeat()
                >>> repeat.repeat_count
                2

        ..  container:: example

            **Example 2.** Unfold repeat:

            ::

                >>> repeat = indicatortools.Repeat(repeat_type='unfold')
                >>> repeat.repeat_count
                2

        Defaults to 2.

        Set to positive integer.

        Returns positive integer.
        '''
        return self._repeat_count

    @property
    def repeat_type(self):
        r'''Gets repeat type of repeat.

        ..  container:: example

            **Example 1.** Volta repeat:

            ::

                >>> repeat = indicatortools.Repeat()
                >>> repeat.repeat_type
                'volta'

        ..  container:: example

            **Example 2.** Unfold repeat:

            ::

                >>> repeat = indicatortools.Repeat(repeat_type='unfold')
                >>> repeat.repeat_type
                'unfold'

        Defaults to ``'volta'``.

        Set to known string.

        Returns string.
        '''
        return self._repeat_type
