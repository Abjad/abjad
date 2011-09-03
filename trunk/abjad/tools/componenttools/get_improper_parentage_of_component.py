def get_improper_parentage_of_component(component):
    '''.. versionadded:: 1.1

    Get improper parentage of `component`::

        abjad> tuplet = Tuplet(Fraction(2, 3), "c'8 d'8 e'8")
        abjad> staff = Staff([tuplet])
        abjad> note = staff.leaves[0]

    ::

        abjad> componenttools.get_improper_parentage_of_component(note)
        (Note("c'8"), Tuplet(2/3, [c'8, d'8, e'8]), Staff{1})

    Return tuple of zero or more components.
    '''

    result = []
    parent = component
    while parent is not None:
        result.append(parent)
        parent = parent._parentage.parent
    result = tuple(result)
    return result
