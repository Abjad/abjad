# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import override
from abjad.tools.functiontools import select
from abjad.tools.scoretools.Context import Context


class Score(Context):
    r'''A score.

    ::

        >>> staff_1 = Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = Staff("c'8 d'8 e'8 f'8")
        >>> score = Score([staff_1, staff_2])
        >>> show(score) # doctest: +SKIP

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, music=None, context_name='Score', name=None):
        Context.__init__(
            self,
            music=music,
            context_name=context_name,
            name=name,
            )
        self.is_simultaneous = True

    ### PUBLIC METHODS ###

    def add_double_bar(self):
        r'''Add double bar to end of score.


            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> score = Score([staff])

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        ::

            >>> score.add_double_bar()
            BarLine('|.')(f'4)

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    f'4
                    \bar "|."
                }
            >>

        ::

            >>> show(score) # doctest: +SKIP

        Returns bar line.
        '''
        from abjad.tools import scoretools
        from abjad.tools import marktools
        from abjad.tools.functiontools import attach
        selection = select(self)
        last_leaf = selection._get_component(scoretools.Leaf, -1)
        double_bar = marktools.BarLine('|.')
        attach(double_bar, last_leaf)
        return double_bar

    def add_final_markup(self, markup, extra_offset=None):
        r'''Add `markup` to end of score:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> score = Score([staff])
            >>> markup = r'\italic \right-column { "Bremen - Boston - LA." "Jul 2010 - May 2011." }'
            >>> markup = markuptools.Markup(markup, Down)
            >>> markup = score.add_final_markup(markup, extra_offset=(4, -2))

        ::

            >>> print format(markup)
            markuptools.Markup((
                markuptools.MarkupCommand(
                    'italic',
                    markuptools.MarkupCommand(
                        'right-column',
                        [
                            'Bremen - Boston - LA.',
                            'Jul 2010 - May 2011.'
                        ]
                        )
                    ),
                ),
                direction=Down
                )

        ..  doctest::

            >>> f(score)
            \new Score <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    \once \override TextScript #'extra-offset = #'(4 . -2)
                    f'4 _ \markup {
                        \italic
                            \right-column
                                {
                                    "Bremen - Boston - LA."
                                    "Jul 2010 - May 2011."
                                }
                        }
                }
            >>

        ::

            >>> show(staff) # doctest: +SKIP

        Return `markup`.
        '''
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        from abjad.tools.functiontools import attach
        selection = select(self)
        last_leaf = selection._get_component(scoretools.Leaf, -1)
        # TODO: copy markup direction from markup input
        markup = markup = markuptools.Markup(markup, Down)
        attach(markup, last_leaf)
        if extra_offset is not None:
            override(last_leaf).text_script.extra_offset = extra_offset
        return markup
