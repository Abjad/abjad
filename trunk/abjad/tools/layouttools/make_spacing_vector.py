from abjad.tools import schemetools


def make_spacing_vector(basic_distance, minimum_distance, padding, stretchability):
    r'''.. versionadded:: 2.0

    Make spacing vector::

        abjad> from abjad.tools import layouttools

    ::

        abjad> layouttools.make_spacing_vector(0, 0, 12, 0)
        SchemeVector((basic_distance . 0), (minimum_distance . 0), (padding . 12), (stretchability . 0))

    Use to set paper block spacing attributes::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> lily_file = lilyfiletools.make_basic_lily_file(staff)
        abjad> lily_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 12, 0)

    ::

        abjad> f(lily_file) # doctest: +SKIP
        % Abjad revision 4229
        % 2011-04-07 15:19

        \version "2.13.44"
        \include "english.ly"
        \include "/abjad/trunk/abjad/cfg/abjad.scm"

        \paper {
            system-system-spacing = #'((basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
        }

        \score {
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        }

    Return scheme vector.
    '''

    return schemetools.SchemeVector(
        schemetools.SchemePair('basic_distance', basic_distance),
        schemetools.SchemePair('minimum_distance', minimum_distance),
        schemetools.SchemePair('padding', padding),
        schemetools.SchemePair('stretchability', stretchability))
