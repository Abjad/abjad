# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


# TODO: remove and just use Spanner instead with overrides
class TextScriptSpanner(Spanner):
    r'''A text script spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> spanner = spannertools.TextScriptSpanner()
        >>> attach(spanner, staff[:])
        >>> spanner.override.text_script.color = 'red'
        >>> markup = markuptools.Markup(r'\italic { espressivo }', Up)
        >>> attach(markup, staff[1])
        Markup((MarkupCommand('italic', ['espressivo']),), direction=Up)(d'8)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \override TextScript #'color = #red
            c'8
            d'8 ^ \markup { \italic { espressivo } }
            e'8
            f'8
            \revert TextScript #'color
        }

    Override LilyPond TextScript grob.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        pass
