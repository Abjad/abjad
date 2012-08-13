from abjad.tools import schemetools


def make_spacing_vector(basic_distance, minimum_distance, padding, stretchability):
    r'''.. versionadded:: 2.0

    Make spacing vector::

        >>> from abjad.tools import layouttools

    ::

        >>> vector = layouttools.make_spacing_vector(0, 0, 12, 0)

    Use to set paper block spacing attributes::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> lilypond_file = lilypondfiletools.make_basic_lilypond_file(staff)
        >>> spacing_vector = layouttools.make_spacing_vector(0, 0, 12, 0)
        >>> lilypond_file.paper_block.system_system_spacing = spacing_vector

    ::

        >>> f(lilypond_file) # doctest: +SKIP
        % Abjad revision 4229
        % 2011-04-07 15:19

        \version "2.13.44"
        \include "english.ly"
        \include "/abjad/trunk/abjad/cfg/abjad.scm"

        \paper {
            system-system-spacing = #'(
                (basic_distance . 0) (minimum_distance . 0) (padding . 12) (stretchability . 0))
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
