import abc
from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDirective(TreeContainer):

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        TreeContainer.__init__(self, children=children, name=name)
        assert isinstance(options, (dict, type(None)))
        self._argument = argument
        self._options = {}
        if options is not None:
            self._options.update(options)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _children_rest_format_contributions(self):
        result = []
        for child in self.children:
            result.append('')
            contribution = child._rest_format_contributions
            for x in contribution:
                if x:
                    result.append('   ' + x)
                else:
                    result.append(x)
        return result

    @property
    def _rest_format_contributions(self):
        if self.argument:
            result = ['.. {}:: {}'.format(self.directive, self.argument)]
        else:
            result = ['.. {}::'.format(self.directive)]
        for key, value in sorted(self.options.items()):
            option = '   :{}:'.format(key)
            if value is True:
                pass
            elif value is None or value is False:
                continue
            elif isinstance(value, (list, tuple)):
                option += ' ' + ', '.join(str(x) for x in value)
            elif isinstance(value, (int, float, str)):
                option += ' ' + str(value)
            result.append(option)
        result.extend(self._children_rest_format_contributions)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def directive(self):
        raise NotImplemented

    @property
    def options(self):
        return self._options

    @property
    def node_klass(self):
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTDirective,
            documentationtools.ReSTHeading,
            documentationtools.ReSTHorizontalRule,
            documentationtools.ReSTParagraph,
            )

    @property
    def rest_format(self):
        return '\n'.join(self._rest_format_contributions)

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def argument():
        def fget(self):
            return self._argument
        def fset(self, arg):
            assert isinstance(arg, (str, type(None)))
            self._argument = arg
        return property(**locals())
