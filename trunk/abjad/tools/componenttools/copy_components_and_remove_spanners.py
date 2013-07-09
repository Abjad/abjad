import copy


def copy_components_and_remove_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Copy `components` and remove spanners.

    The `components` must be thread-contiguous.

    The steps taken by this function are as follows:

    * Withdraw `components` from spanners.

    * Deep copy unspanned `components`.

    * Reapply spanners to `components`.

    * Return copied components.

    Example 1. Copy components one time:

    ::

        >>> voice = Voice("abj: | 2/4 c'4 ( d' || 2/4 e' f' ) |")

    ::

        >>> f(voice)
        \new Voice {
            {
                \time 2/4
                c'4 (
                d'4
            }
            {
                e'4
                f'4 )
            }
        }

    ::

        >>> show(voice) # doctest: +SKIP

    ::

        >>> result = componenttools.copy_components_and_remove_spanners(
        ...     voice.leaves[1:3])

    ::

        >>> result
        Selection(Note("d'4"), Note("e'4"))

    ::

        >>> new_voice = Voice(result)

    ::

        >>> show(new_voice) # doctest: +SKIP

    ::

        >>> f(new_voice)
        \new Voice {
            d'4
            e'4
        }

    ::

        >>> voice.leaves[2] is new_voice.leaves[0]
        False

    Example 2. Copy components multiple times:

    ::

        >>> result = componenttools.copy_components_and_remove_spanners(
        ...     voice.leaves[1:3], n=2)

    ::

        >>> new_voice = Voice(result)

    ::

        >>> show(new_voice) # doctest: +SKIP

    ::

        >>> f(new_voice)
        \new Voice {
            d'4
            e'4
            d'4
            e'4
        }

    Return selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import selectiontools

    # check input
    assert componenttools.all_are_thread_contiguous_components(components)

    # return empty selection when nothing to copy
    if n < 1:
        return selectiontools.Selection()

    # copy components without spanners
    result = []
    for component in components:
        new = component._copy_with_children_and_marks_but_without_spanners()
        result.append(new)

    # repeat as necessary
    for i in range(n - 1):
        result += copy_components_and_remove_spanners(components)

    # set result type
    result = type(components)(result)

    # return result
    return result
