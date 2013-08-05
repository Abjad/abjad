# -*- encoding: utf-8 -*-
def select_tuplets(
    expr=None,
    include_augmented_tuplets=True,
    include_diminished_tuplets=True,
    include_trivial_tuplets=True,
    recurse=True,
    tuplet_classes=None,
    ):
    r'''Select tuplets in `expr`.

        >>> staff = Staff()
        >>> staff.extend(r"c'8 d'8 \times 2/3 { e'8 g'8 f'8 }")
        >>> staff.extend(r"g'8 f'8 \times 2/3 { e'8 c'8 d'8 }")

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            \times 2/3 {
                e'8
                g'8
                f'8
            }
            g'8
            f'8
            \times 2/3 {
                e'8
                c'8
                d'8
            }
        }


    ::

        >>> show(staff) # doctest: +SKIP

    ::

        >>> selection = selectiontools.select_tuplets(staff)

    ::

        >>> selection
        FreeTupletSelection(...)

    ::

        >>> for tuplet in selection:
        ...     tuplet
        Tuplet(2/3, [e'8, g'8, f'8])
        Tuplet(2/3, [e'8, c'8, d'8])

    Return tuplet selection.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import selectiontools
    from abjad.tools import tuplettools
    expr = expr or []
    tuplet_classes = tuplet_classes or (tuplettools.Tuplet,)
    if recurse:
        expr = iterationtools.iterate_tuplets_in_expr(expr)
    tuplets = []
    for tuplet in expr:
        if (not include_augmented_tuplets and tuplet.is_augmentation) or \
        (not include_diminished_tuplets and tuplet.is_diminution) or \
        (not include_trivial_tuplets and tuplet.is_trivial) or \
        not isinstance(tuplet, tuplet_classes):
            continue
        else:
            tuplets.append(tuplet)
    selection = selectiontools.FreeTupletSelection(music=tuplets)
    return selection
