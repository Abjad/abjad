from experimental.divisiontools.VoiceDivisionList import VoiceDivisionList


class SegmentDivisionList(VoiceDivisionList):
    r'''.. versionadded:: 1.0

    Segment division lists model the **parts of** all
    divisions that intersect some segment.

    Segment division lists break divisions that cross segment boundaries.

    Segment division lists contrast with division region division lists.
    The best way to show this is with an example::

        >>> from abjad import *
        >>> from experimental import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
        >>> score_specification = specificationtools.ScoreSpecification(score_template)
        >>> segment = score_specification.append_segment('red')

    ::

        >>> setting = segment.set_time_signatures([(4, 8), (3, 8)])
        >>> setting = segment.set_divisions([(3, 16)], contexts=segment.v1)
        >>> setting = segment.set_rhythm(library.thirty_seconds)

    ::

        >>> segment = score_specification.append_segment('blue')
        >>> segment = score_specification.append_segment('green')

    ::

        >>> score = score_specification.interpret()


    ``'Voice 1'`` has only one division region division list::

        >>> len(score_specification.contexts['Voice 1']['division_region_division_lists'])
        1

    ::

        >>> z(score_specification.contexts['Voice 1']['division_region_division_lists'][0])
        divisiontools.DivisionRegionDivisionList(
            [Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
            Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
            Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), Division('[3, 16]'), 
            Division('[3, 16]'), Division('[3, 16]')],
            'Voice 1',
            start_timepoint=timespantools.SymbolicTimepoint(
                selector=selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                offset=durationtools.Offset(0, 1)
                ),
            stop_timepoint=timespantools.SymbolicTimepoint(
                selector=selectortools.SingleSegmentSelector(
                    identifier='red'
                    ),
                offset=durationtools.Offset(21, 8)
                )
            )

    The reason that ``'Voice 1'`` has only one division region division list is that the 
    composer specified only one division-maker for the entire score.

    But ``'Voice 1'`` has three different segment division lists::

        >>> for x in score_specification.contexts['Voice 1']['segment_division_lists']: x
        ... 
        SegmentDivisionList('[3, 16], [3, 16], [3, 16], [3, 16], [2, 16)')
        SegmentDivisionList('(1, 16], [3, 16], [3, 16], [3, 16], [3, 16], [1, 16)')
        SegmentDivisionList('(2, 16], [3, 16], [3, 16], [3, 16], [3, 16]')

    The reason that ``'Voice 1'`` has three different segment division lists
    is that the composer specified three different segments.

    Note that composers may specify an arbitrary number of division-makers for any given voice.
    This results in an arbitrary number of division regions per voice.

    Note also that composers may specify an arbitrary number of segments per score.
    This results in an arbtirary number of segments per voice.

    Taken together these two facts mean that the division region division lists attaching 
    to a voice and the segment division lists attaching to that same voice do not 
    relate to each other in any systematic way.

    Composers do not create segment division lists because all division lists
    arise as byproducts of interpretation.
    '''

    pass
