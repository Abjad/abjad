from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.Division import Division


class DivisionList(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, divisions):
        assert isinstance(divisions, list), divisions
        self._divisions = [Division(x) for x in divisions]
        assert self.is_well_formed

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        assert isinstance(expr, type(self)), expr
        assert self.is_right_open, self
        assert expr.is_left_open, expr
        divisions = []
        divisions.extend(self[:-1])
        divisions.append(self[-1] + expr[0])
        divisions.extend(expr[1:])
        return type(self)(divisions, is_left_open=self.is_left_open, is_right_open=expr.is_right_open)

    def __getitem__(self, expr):
        return self.divisions.__getitem__(expr)

    def __len__(self):
        return len(self.divisions)

    ### READ-ONLY PROPERTIES ###

    @property
    def divisions(self):
        return self._divisions

    @property
    def is_closed(self):
        return self.is_left_closed and self.is_right_closed

    @property
    def is_half_closed(self):
        return not self.is_left_closed == self.is_right_closed

    @property
    def is_half_open(self):
        return not self.is_left_open == self.is_right_open

    @property
    def is_left_closed(self):
        return self[0].is_left_closed

    @property
    def is_left_open(self):
        return self[0].is_left_open

    @property
    def is_right_closed(self):
        return self[-1].is_right_closed

    @property
    def is_right_open(self):
        return self[-1].is_right_open

    @property
    def is_open(self):
        return not self.is_left_closed and not self.is_right_closed

    @property
    def is_well_formed(self):
        if 1 < len(self) and self[0].is_right_open:
            return False
        if 1 < len(self) and self[-1].is_left_open:
            return False
        return True

    @property
    def pairs(self):
        return [division.pair for division in self]
