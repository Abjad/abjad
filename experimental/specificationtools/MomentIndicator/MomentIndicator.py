from abjad.tools.abctools.AbjadObject import AbjadObject
from specificationtools.Selection import Selection


class MomentIndicator(AbjadObject):
    '''Model of any single moment in the middle of some selection somewhere.

    The way this works is that first a selection is made.
    Then the criterion specifies how to iterate or otherwise inspect the selection.
    (Default criterion is probably something like all components.)
    Then count specifies which component to fetch during iteration or inspection.
    (Default count is probably 0 for the first component encountered.)
    Then boundary condition specifies whether the moment to be retrieved should
    be just before, exactly coincident with or just after a time point taken equal
    to either component start time or component stop time.
    (Default boundary condition is probably the moment exactly coincident with
    component start time.)
    
    MomentIndicator notionally models an infinitely thing vertical cursor
    placed over the graphic selection of any score segment.
    '''

    ### INITIALIZER ###

    def __init__(self, selection, criterion=None, count=None, boundary_condition=None):
        assert isinstance(selection, Selection)
        assert isinsstance(count, (int, type(None)))
        self.selection = selection
        self.criterion = criterion
        self.count = count
        self.boundary_condition = boundary_condition
