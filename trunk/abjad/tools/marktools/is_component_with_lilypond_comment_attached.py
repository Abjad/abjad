from abjad.tools import componenttools


def is_component_with_lilypond_comment_attached(expr, comment_contents_string=None):
    '''.. versionadded:: 2.3

    True when `expr` is component with LilyPond comment mark attached::

        >>> note = Note("c'4")
        >>> marktools.LilyPondComment('comment here')(note)
        LilyPondComment('comment here')(c'4)

    ::

        >>> marktools.is_component_with_lilypond_comment_attached(note)
        True

    False otherwise::

        >>> note = Note("c'4")

    ::

        >>> marktools.is_component_with_lilypond_comment_attached(note)
        False

    Return boolean.
    '''
    from abjad.tools import marktools

    if isinstance(expr, componenttools.Component):
        for comment in marktools.get_lilypond_comments_attached_to_component(expr):
            if comment.contents_string == comment_contents_string or \
                comment_contents_string is None:
                return True

    return False
