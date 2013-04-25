import abc
from abjad.tools import iotools
from abjad.tools.abctools.AbjadObject import AbjadObject


class Specifier(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    def __init__(self, description=None, name=None, source=None):
        self.description = description
        self.name = name
        self.source = source

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if self is other:
            return True
        if isinstance(other, type(self)):
            if self._positional_argument_values == other._positional_argument_values:
                if self._keyword_argument_name_value_strings == other._keyword_argument_name_value_strings:
                    return True
        return False

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _human_readable_class_name(self):
        return iotools.uppercamelcase_to_space_delimited_lowercase(self._class_name)

#    @property
#    def _keyword_argument_names(self):
#        '''Defined by hand so that this tuple is inheritable by subclasses.
#        Is there a way to derive this programmatically *and* be inheritable by subclasses?
#        '''
#        return tuple(sorted([
#            'description',
#            'name',
#            ]))

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def format(self):
        return self._tools_package_qualified_indented_repr

    @abc.abstractproperty
    def one_line_menuing_summary(self):
        pass
