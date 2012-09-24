from abjad.tools import marktools


def set_accidental_style_on_sequential_contexts_in_expr(expr, accidental_style):
    r'''.. versionadded:: 2.0

    Set `accidental_style` for sequential semantic contexts in `expr`::

        >>> score = Score(Staff("c'8 d'8") * 2)
        >>> contexttools.set_accidental_style_on_sequential_contexts_in_expr(score, 'forget')

    ::

        >>> f(score)
        \new Score <<
            \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
            }
            \new Staff {
                #(set-accidental-style 'forget)
                c'8
                d'8
            }
        >>

    Skip nonsemantic contexts.

    Function looks like a hack but isn't.
    LilyPond uses the dedicated command shown here to set accidental style.
    This means that it is not possible to set accidental style on
    a top-level context like score with a single override.
    '''
    from abjad.tools import contexttools
    from abjad.tools import iterationtools

    for context in iterationtools.iterate_components_in_expr(expr, contexttools.Context):
        if context.is_semantic:
            if not context.is_parallel:
                marktools.LilyPondCommandMark("#(set-accidental-style '%s)" % accidental_style)(context)
