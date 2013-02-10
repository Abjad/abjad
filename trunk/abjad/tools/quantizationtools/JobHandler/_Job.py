from abjad.tools import mathtools
from abjad.tools.abctools import AbjadObject


class _Job(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, number):
        self.number = number

    ### SPECIAL METHODS ###

    def __call__(self):
        self.result = [x for x in mathtools.yield_all_compositions_of_integer(self.number)]

    def __repr__(self):
        return '{}({})'.format(self._class_name, self.number)
