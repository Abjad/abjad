from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentSpecificationInventory(AbjadObject, list):
    r'''.. versionadded:: 1.0

    Segment specification inventory.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        list.__init__(self, *args)

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return list.__getitem__(self, arg)
        elif isinstance(arg, str):
            for segment in self:
                if segment.segment_name == arg:
                    return segment
            else:
                raise KeyError(repr(arg))

    def __repr__(self):
        return '{}({})'.format(self._class_name, list.__repr__(self))
