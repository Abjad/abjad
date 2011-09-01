from abjad.tools.marktools.get_lilypond_comments_attached_to_component import get_lilypond_comments_attached_to_component


def is_component_with_lilypond_comment_attached(expr, comment_contents_string = None):
    '''.. versionadded:: 2.3

    True when `expr` is component with LilyPond comment mark attached::

        abjad> note = Note("c'4")
        abjad> marktools.LilyPondComment('comment here')(note)
        LilyPondComment('comment here')(c'4)

    ::

        abjad> marktools.is_component_with_lilypond_comment_attached(note)
        True

    False otherwise::

        abjad> note = Note("c'4")

    ::

        abjad> marktools.is_component_with_lilypond_comment_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools.componenttools._Component import _Component

    if isinstance(expr, _Component):
        for comment in get_lilypond_comments_attached_to_component(expr):
            if comment.contents_string == comment_contents_string or \
                comment_contents_string is None:
                return True

    return False
