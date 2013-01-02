import abc
from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDirective(TreeContainer):

    ### INITIALIZER ###

    def __init__(self, argument=None, children=None, name=None, options=None):
        TreeContainer.__init__(self, children=children, name=name)
        assert isinstance(options, (dict, type(None)))
        self._argument = argument
        self._options = {}
        self._options.update(options)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _rest_format_contributions(self):
        result = ['.. {}::'.format(self.directive)]
        if self.argument:
            result[0] += ' {}'.format(self.argument)
        for key, value in sorted(self.options.items()):
            option = '   :{}:'.format(key)
            if value is not None:
                option += ' {}'.format(value)
            result.append(option)
        for child in self.children:
            result.append('')
            contribution = child._rest_format_contributions
            for x in contribution:
                if x:   
                    result.append('   ' + x)
                else:
                    result.append(x)
        result.append('')
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

    ### READ/WRITE PUBLIC PROPERTIES ###

    @apply
    def argument():
        def fget(self):
            return self._argument
        def fset(self, arg):
            assert isinstance(arg, (str, type(None)))
            self._argument = arg
        return property(**locals())
