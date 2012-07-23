from experimental.interpretationtools.DivisionList import DivisionList


class SegmentDivisionList(DivisionList):
    r'''.. versionadded:: 1.0

    A segment division list is a type of division list.

    Right now segment division lists model all divisions that **intersect**
    some segment.

    Because of this segment division lists break divisions that cross segment boundaries.

    (Segment division lists will probably migrate later to model
    all divisions that **start during** some segment instead.)

    Segment division lists contrast with division region division lists.
    The best way to show this is with an example::

        >>> from abjad.tools import *
        >>> from experimental.specificationtools import library
        >>> from experimental.specificationtools import ScoreSpecification

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
        >>> specification = ScoreSpecification(score_template)
        >>> segment = specification.append_segment()

    ::

        >>> setting = segment.set_time_signatures(segment, [(4, 8), (3, 8)])
        >>> setting = segment.set_divisions(segment.v1, [(3, 16)])
        >>> setting = segment.set_rhythm(segment, library.thirty_seconds)

    ::

        >>> segment = specification.append_segment()
        >>> segment = specification.append_segment()

    ::

        >>> score = specification.interpret()

    Notice that ``'Voice 1'`` has only one division region division list.

    The reason for this is that the composer specified only one division-maker
    for the entire score::

        >>> for x in specification.payload_context_dictionary['Voice 1']['region_division_lists']: x
        ... 
        DivisionRegionDivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    But notice that ``'Voice 1'`` has three different segment division lists.

    The reason for this is that the composer specified three different segments::

        >>> for x in specification.payload_context_dictionary['Voice 1']['segment_division_lists']: x
        ... 
        SegmentDivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [2, 16)')
        SegmentDivisionList('(1, 16], [3, 16], [3, 16], [3, 16], [3, 16], [1, 16)')
        SegmentDivisionList('(2, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    Composers may specify an arbitrary number of division-makers for any given voice.
    This results in an arbitrary number of division regions per voice.

    Composers may specify an arbitrary number of segments per score.
    This results in an arbtirary number of segments per voice.

    Taken together these two facts mean that the division region division lists attaching 
    to a voice and the segment division lists attaching to that same voice do not 
    relate to each other in any systematic way.
    '''

    pass
