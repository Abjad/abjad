from experimental.interpretertools.UninterpretedDivisionCommand import UninterpretedDivisionCommand


class SegmentDivisionCommand(UninterpretedDivisionCommand):
    r'''.. versionadded:: 1.0

    Previously only zero or one division setting could be made per segment.

    Now zero or more division settings can be made per segment.

    What does this mean?

    This means that the meaning of a segment division token is currently
    shifting from "**the** division setting active during segment"
    to "**one** (of possibly many) division settings active during segment".
    '''

    pass
