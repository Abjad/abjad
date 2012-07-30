from abjad.tools import abctools
from abjad.tools import mathtools


class _Job(abctools.AbjadObject):

    def __init__(self, number):
        self.number = number

    def __call__(self):
        self.result = [x for x in mathtools.yield_all_compositions_of_integer(self.number)]

    def __repr__(self):
        return '{}({})'.format(self._class_name, self.number)
