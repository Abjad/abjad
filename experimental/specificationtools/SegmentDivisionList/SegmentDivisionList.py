from specificationtools.DivisionList import DivisionList


class SegmentDivisionList(DivisionList):
    '''Segment division list is a type of division list.

    Composers do not specify segment division lists; rather, 
    segment division lists arise during interpretation.

    Like other division lists, segment division lists are attributes of a voice.

    Segment division lists contrast with region division lists.
    The best way to show this is with an example::

        >>> from specificationtools import ScoreSpecification

        >>> specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))

        >>> segment = specification.append_segment()
        >>> segment.set_time_signatures(segment, [(4, 8), (3, 8)])
        >>> segment.set_divisions(segment.v1, [(3, 16)])
        >>> segment.set_rhythm(segment, library.thirty_seconds)

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
        SegmentDivisionList([D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(2, 16))])
        SegmentDivisionList([D((1, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16), D(1, 16))])
        SegmentDivisionList([D((2, 16), D(3, 16), D(3, 16), D(3, 16), D(3, 16)])

    After interpretation each voice carries exactly one segment division list per segment.
    
    (In this example voice 1 carries three segment division list because the score comprises three segments.)

    Segments division lists show the divisions belonging to a voice broken by score segment.

    The broken view that segment division lists provide will frequently be at odds with the
    unbroken divisions contained in the region division list belonging to a voice.
    '''

    pass
