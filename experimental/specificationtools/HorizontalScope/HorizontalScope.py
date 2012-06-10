from abjad.tools import componenttools
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class HorizontalScope(AbjadObject):

    ### CLASS ATTRIBUTES ###

    criteria_strings = ('divisions', 'measures',)

    ### INITIALIZER ###

    def __init__(self, criterion, part=None, start=None, stop=None):
        assert self.is_valid_criterion(criterion)
        assert self.is_valid_part_token(part)
        assert isinstance(start, (int, type(None)))
        assert isinstance(stop, (int, type(None)))
        assert self.are_concordant_input_values(part, start, stop)
        self.criterion = criterion
        self.part = part
        self.start = start
        self.stop = stop

    ### PUBLIC METHODS ###

    def all_are_component_subclasses(self, expr):
        try:
            return all([issubclass(x, componenttools.Component) for x in expr])
        except:
            return False

    def are_concordant_input_values(self, part, start, stop):
        if part is not None:
            if start is not None or stop is not None:
                return False
        return True
        
    def is_valid_criterion(self, expr):
        if expr is None:
            return True
        elif self.all_are_component_subclasses(expr):
            return True
        elif expr in self.criteria_strings:
            return True
        else:
            raise ValueError('invalid temporal scope criterion: {!r}'.format(expr))

    def is_valid_part_token(self, expr):
        if expr is None:
            return True
        elif isinstance(expr, (tuple, list)) and len(expr) == 2:
            if all([mathtools.is_integer_equivalent_number(x) for x in expr[0]]):
                if mathtools.is_integer_equivalent_number(expr[1]):
                    return True
        return False
