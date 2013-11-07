# -*- encoding: utf-8 -*-
import types


def iterate_runs_in_expr(sequence, classes):
    r'''Iterate runs in expression.
    
    ..  container:: example
    
        **Example 1.** Iterate runs of notes and chords at only the 
        top level of score:

        ::

            >>> staff = Staff(r"\times 2/3 { c'8 d'8 r8 }")
            >>> staff.append(r"\times 2/3 { r8 <e' g'>8 <f' a'>8 }")
            >>> staff.extend("g'8 a'8 r8 r8 <b' d''>8 <c'' e''>8")

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \times 2/3 {
                    c'8
                    d'8
                    r8
                }
                \times 2/3 {
                    r8
                    <e' g'>8
                    <f' a'>8
                }
                g'8
                a'8
                r8
                r8
                <b' d''>8
                <c'' e''>8
            }

        ::

            >>> for group in iterationtools.iterate_runs_in_expr(
            ...     staff[:], (Note, Chord)):
            ...     group
            (Note("g'8"), Note("a'8"))
            (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    ..  container:: example

        **Example 2.** Iterate runs of notes and chords at all levels of score:

        ::

            >>> leaves = iterate(staff).by_class(scoretools.Leaf)

        ::

            >>> for group in iterationtools.iterate_runs_in_expr(
            ...     leaves, (Note, Chord)):
            ...     group
            (Note("c'8"), Note("d'8"))
            (Chord("<e' g'>8"), Chord("<f' a'>8"), Note("g'8"), Note("a'8"))
            (Chord("<b' d''>8"), Chord("<c'' e''>8"))

    Returns generator.
    '''
    from abjad.tools import scoretools
    from abjad.tools import selectiontools

    assert isinstance(sequence, (
        list,
        tuple,
        types.GeneratorType, 
        selectiontools.Selection)), repr(sequence)

    sequence = selectiontools.SliceSelection(sequence)

    current_group = ()
    for group in sequence.group_by(type):
        if type(group[0]) in classes:
            current_group = current_group + group
        elif current_group:
            yield current_group
            current_group = ()

    if current_group:
        yield current_group
