def _give_spanners_that_dominate_donor_components_to_recipient_components(
    donors, recipients):
    '''Find all spanners dominating donors.
    Insert each component in recipients into
    each spanner dominating donors.
    Remove donors from each dominating spanner.
    Return none.
    Not composer-safe.
    '''
    from abjad.tools import componenttools
    from abjad.tools import spannertools
    assert componenttools.all_are_thread_contiguous_components(donors)
    assert componenttools.all_are_thread_contiguous_components(recipients)
    receipt = spannertools.get_spanners_that_dominate_components(donors)
    for spanner, index in receipt:
        for recipient_component in reversed(recipients):
            spanner._insert(index, recipient_component)
        for donor_component in donors:
            spanner._remove(donor_component)
