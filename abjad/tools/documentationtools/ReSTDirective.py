# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TreeContainer import TreeContainer


class ReSTDirective(TreeContainer):
    r'''A ReST directive.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'reStructuredText'

    ### INITIALIZER ###

    def __init__(
        self,
        argument=None,
        children=None,
        directive=None,
        name=None,
        options=None,
        ):
        TreeContainer.__init__(self, children=children, name=name)
        assert isinstance(options, (dict, type(None)))
        self._argument = argument
        self._options = {}
        if options is not None:
            self._options.update(options)
        self._directive = directive

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        for name in ('children', 'name', 'options'):
            if not getattr(self, name, None) and name in names:
                names.remove(name)
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_kwargs_names=names,
            )

    ### PRIVATE PROPERTIES ###

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

    ### PUBLIC PROPERTIES ###

    @property
    def argument(self):
        r'''Gets and sets argument of ReST directive.
        '''
        return self._argument

    @argument.setter
    def argument(self, arg):
        assert isinstance(arg, (str, type(None)))
        self._argument = arg

    @property
    def directive(self):
        r'''Gets and sets directive of ReST directive.
        '''
        return self._directive

    @directive.setter
    def directive(self, expr):
        self._directive = str(expr)

    @property
    def node_class(self):
        r'''Node class of ReST directive.
        '''
        from abjad.tools import documentationtools
        return (
            documentationtools.ReSTDirective,
            documentationtools.ReSTHeading,
            documentationtools.ReSTHorizontalRule,
            documentationtools.ReSTParagraph,
            )

    @property
    def options(self):
        r'''Options of ReST directive.
        '''
        return self._options

    @property
    def rest_format(self):
        r'''ReST format of ReST directive.
        '''
        return '\n'.join(self._rest_format_contributions)
