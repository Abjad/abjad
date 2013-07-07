def _give_children_from_donor_components_to_empty_container(
    donors, recipient):
    '''Give any music belong to donor components 'donors'
    to recipient component 'recipient'.
    Works great when 'recipient' is an empty container.
    Pass silently when recipient is a nonempty container
    or a leaf and when donors have no music.
    Raises music contents error when donors *do* have music
    to music but when recipient is unable to accept music
    (because recipient is nonempty container or leaf).
    Return none.

    Not composer-safe.
    '''
    from abjad.tools import componenttools
    from abjad.tools import containertools
    from abjad.tools import leaftools

    # check input
    assert componenttools.all_are_contiguous_components_in_same_parent(donors)
    assert isinstance(recipient, containertools.Container), repr(recipient)
    assert len(recipient) == 0

    # otherwise recipient is empty container,
    # so proceed to collect music from all donor components
    donor_music = []
    for donor in donors:
        donor_music.extend(getattr(donor, 'music', ()))

    # give music from donor components to recipient component
    recipient._music.extend(donor_music)
    recipient[:]._set_component_parents(recipient)
