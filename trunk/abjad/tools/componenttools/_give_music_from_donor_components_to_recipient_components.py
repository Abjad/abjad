from abjad.exceptions import MusicContentsError
from abjad.tools.componenttools._switch_components_to_parent import _switch_components_to_parent


def _give_music_from_donor_components_to_recipient_components(donors, recipient):
    '''Give any music belong to donor components 'donors'
    to recipient component 'recipient'.
    Works great when 'recipient' is an empty container.
    Pass silently when recipient is a nonempty container
    or a leaf and when donors have no music.
    Raises music contents error when donors *do* have music
    to music but when recipient is unable to accept music
    (because recipient is nonempty container or leaf).

    Return donor components 'donors'.

    Helper is not composer-safe and may cause discontiguous spanners.
    '''
    from abjad.tools.containertools.Container import Container
    from abjad.tools.leaftools._Leaf import _Leaf
    from abjad.tools import componenttools

    assert componenttools.all_are_contiguous_components_in_same_parent(donors)

    # if recipient is leaf or nonempty container,
    # make sure there's no music in donor components to hand over
    if isinstance(recipient, _Leaf) or \
        (isinstance(recipient, Container) and len(recipient)):
        if all([len(x.music) == 0 for x in donors]):
            return donors
        else:
            raise MusicContentsError('can not give music to leaf: "%s".' % recipient)

    # otherwise recipient is empty container, so proceed
    # collect music from all donor components
    donor_music = []
    for donor in donors:
        #donor_music.extend(donor.music)
        donor_music.extend(getattr(donor, 'music', ()))

    # give music from donor components to recipient component
    recipient._music.extend(donor_music)
    _switch_components_to_parent(recipient[:], recipient)

    # return donor components
    return donors
