from experimental.specificationtools.DivisionList import DivisionList


class SegmentDivisionList(DivisionList):
    '''Segment division list is a type of division list.

    Composers do not specify segment division lists; rather, 
    segment division lists arise during interpretation.

    Like other division lists, segment division lists are attributes of a voice.

    Segment division lists contrast with region division lists.
    The best way to show this is with an example::

        >>> from abjad.tools import *
        >>> from experimental.specificationtools import library
        >>> from experimental.specificationtools import ScoreSpecification

        >>> specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
        >>> segment = specification.append_segment()

        >>> segment.set_time_signatures(segment, [(4, 8), (3, 8)])
        Directive(Selection(contexts=['Grouped Rhythmic Staves Score'], scope=TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Left), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Right))), 'time_signatures', [(4, 8), (3, 8)], persistent=True, truncate=False)

        >>> segment.set_divisions(segment.v1, [(3, 16)])
        Directive(Selection(contexts=['Voice 1'], scope=TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Left), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Right))), 'divisions', [(3, 16)], persistent=True, truncate=False)

        >>> segment.set_rhythm(segment, library.thirty_seconds)
        Directive(Selection(contexts=['Grouped Rhythmic Staves Score'], scope=TemporalScope(start=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Left), stop=TemporalCursor(anchor=ScoreObjectIndicator(segment='1'), edge=Right))), 'rhythm', OutputBurnishedSignalFilledTimeTokenMaker('thirty_seconds'), persistent=True, truncate=False)

        >>> segment = specification.append_segment()
        >>> segment = specification.append_segment()

        >>> score = specification.interpret()

    After interpretation voice 1 has only one region division list::

        >>> for x in specification.payload_context_dictionary['Voice 1']['region_division_lists']: x
        ... 
        RegionDivisionList([D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16)])

    But voice 1 has three segment division lists::

        >>> for x in specification.payload_context_dictionary['Voice 1']['segment_division_lists']: x
        ... 
        SegmentDivisionList([D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(2, 16))], is_right_open=True)
        SegmentDivisionList([D((1, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(1, 16))], is_left_open=True, is_right_open=True)
        SegmentDivisionList([D((2, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16)], is_left_open=True)

    After interpretation each voice carries exactly one segment division list per segment.
    
    (In this example voice 1 carries three segment division list because the score comprises three segments.)

    Segments division lists show the divisions belonging to a voice broken by score segment.

    The broken view that segment division lists provide will frequently be at odds with the
    unbroken divisions contained in the region division list belonging to a voice.
    '''

    pass
