# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate
from abjad.tools.topleveltools import override
from abjad.tools.topleveltools import select
from abjad.tools.scoretools.Context import Context


class Score(Context):
    r'''A score.

    ::

        >>> staff_1 = Staff("c'8 d'8 e'8 f'8")
        >>> staff_2 = Staff("c'8 d'8 e'8 f'8")
        >>> score = Score([staff_1, staff_2])
        >>> show(score) # doctest: +SKIP

    ..  doctest::

        >>> print(format(score))
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

    __documentation_section__ = 'Contexts'

    __slots__ = ()

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

    def add_final_bar_line(
        self, 
        abbreviation='|.',
        to_each_voice=False,
        ):
        r'''Add final bar line to end of score.


            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> score = Score([staff])

        ..  doctest::

            >>> print(format(score))
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

            >>> score.add_final_bar_line()
            BarLine('|.')

        ..  doctest::

            >>> print(format(score))
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

        Set `to_each_voice` to true to make part extraction easier.

        Returns bar line.
        '''
        from abjad.tools import scoretools
        from abjad.tools import indicatortools
        double_bar = indicatortools.BarLine(abbreviation)
        if not to_each_voice:
            selection = select(self)
            last_leaf = selection._get_component(scoretools.Leaf, -1)
            attach(double_bar, last_leaf)
        else:
            for voice in iterate(self).by_class(scoretools.Voice):
                selection = select(voice)
                last_leaf = selection._get_component(scoretools.Leaf, -1)
                attach(double_bar, last_leaf)
        return double_bar

    def add_final_markup(self, markup, extra_offset=None):
        r'''Adds `markup` to end of score:

        ::

            >>> staff = Staff("c'4 d'4 e'4 f'4")
            >>> score = Score([staff])
            >>> place = Markup('Bremen - Boston - LA.', direction=Down)
            >>> date = Markup('Jul 2010 - May 2011.')
            >>> markup = Markup.right_column([place, date], direction=Down)
            >>> markup = markup.italic()
            >>> markup = score.add_final_markup(markup, extra_offset=(0.5, -2))

        ::

            >>> print(format(markup))
            _ \markup {
                \italic
                    \right-column
                        {
                            "Bremen - Boston - LA."
                            "Jul 2010 - May 2011."
                        }
                }

        ..  doctest::

            >>> print(format(score))
            \new Score <<
                \new Staff {
                    c'4
                    d'4
                    e'4
                    \once \override TextScript #'extra-offset = #'(0.5 . -2)
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

        Returns `markup`.
        '''
        from abjad.tools import markuptools
        from abjad.tools import scoretools
        selection = select(self)
        last_leaf = selection._get_component(scoretools.Leaf, -1)
        # TODO: copy markup direction from markup input
        markup = markup = markuptools.Markup(markup, Down)
        attach(markup, last_leaf)
        if extra_offset is not None:
            override(last_leaf).text_script.extra_offset = extra_offset
        return markup