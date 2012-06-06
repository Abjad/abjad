from abjad.tools.abctools.AbjadObject import AbjadObject


class SegmentInventory(AbjadObject, list):

    ### INITIALIZER ###

    def __init__(self, *args):
        list.__init__(self, *args)

    ### SPECIAL METHODS ###

    def __getitem__(self, arg):
        if isinstance(arg, int):
            return list.__getitem__(self, arg)
        elif isinstance(arg, str):
            for segment in self:
                if segment.name == arg:
                    return segment
            else:
                raise KeyError(repr(arg))

    def __repr__(self):
        return '{}({})'.format(self._class_name, list.__repr__(self))
