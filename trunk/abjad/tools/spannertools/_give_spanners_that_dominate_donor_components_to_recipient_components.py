from abjad.tools.spannertools.get_spanners_that_dominate_components import get_spanners_that_dominate_components


def _give_spanners_that_dominate_donor_components_to_recipient_components(donor_components, recipient_components):
    '''Find all spanners dominating 'donor_components'.
        Insert each component in 'recipient_components' into
        each spanner dominating 'donor_components'.
        Remove 'donor_components' from each dominating spanner.
        Return 'donor_components'.

        Not composer-safe.
    '''
    from abjad.tools import componenttools

    assert componenttools.all_are_thread_contiguous_components(donor_components)
    assert componenttools.all_are_thread_contiguous_components(recipient_components)

    receipt = get_spanners_that_dominate_components(donor_components)
    for spanner, index in receipt:
        for recipient_component in reversed(recipient_components):
            spanner._insert(index, recipient_component)
        for donor_component in donor_components:
            spanner._remove(donor_component)

    return donor_components
