from abjad.tools import durationtools
from abjad.tools.mathtools import greatest_power_of_two_less_equal
from abjad.tools.sequencetools.truncate_runs_in_sequence import truncate_runs_in_sequence


# TODO: Maybe move get_likely_multiplier_of_components() from durationtools to measuretools? #

def get_likely_multiplier_of_components(components):
    r'''.. versionadded:: 2.0

    Get likely multiplier of `components`::

        abjad> staff = Staff("c'8.. d'8.. e'8.. f'8..")
        abjad> f(staff)
        \new Staff {
            c'8..
            d'8..
            e'8..
            f'8..
        }
        abjad> componenttools.get_likely_multiplier_of_components(staff[:])
        Duration(7, 4)

    Return 1 when no multiplier is likely::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
        abjad> componenttools.get_likely_multiplier_of_components(staff[:])
        Duration(1, 1)

    Return none when more than one multiplier is likely::

        abjad> staff = Staff(notetools.make_notes([0, 2, 4, 5], [(3, 16), (7, 32)]))
        abjad> f(staff)
        \new Staff {
            c'8.
            d'8..
            e'8.
            f'8..
        }
        abjad> componenttools.get_likely_multiplier_of_components(staff[:]) is None
        True

    Return fraction or none.
    '''
    from abjad.tools import componenttools
    from abjad.tools import tietools

    assert componenttools.all_are_components(components)

    chain_duration_numerators = []
    for expr in tietools.iterate_topmost_tie_chains_and_components_forward_in_expr(components):
        if tietools.is_tie_chain(expr):
            chain_duration = tietools.get_preprolated_tie_chain_duration(expr)
            chain_duration_numerators.append(chain_duration.numerator)

    if len(truncate_runs_in_sequence(chain_duration_numerators)) == 1:
        numerator = chain_duration_numerators[0]
        denominator = greatest_power_of_two_less_equal(numerator)
        likely_multiplier = durationtools.Duration(numerator, denominator)
        return likely_multiplier
