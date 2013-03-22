from abjad.tools.abctools import AbjadObject


class SimpleInequality(AbjadObject):
    '''.. versionadded:: 2.12

    Simple inequality.

        >>> template = 'timespan_2.start < timespan_1.start'
        >>> simple_inequality = timerelationtools.SimpleInequality(template)

    ::

        >>> simple_inequality
        SimpleInequality('timespan_2.start < timespan_1.start')

    Return simple inequality.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_template', )

    ### INITIALIZER ###

    def __init__(self, template):
        assert isinstance(template, str), repr(template)
        self._template = template

    ### PRIVATE METHODS ###

    # do not indent storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return [''.join(
            AbjadObject._get_tools_package_qualified_repr_pieces(self, is_indented=False))]

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def storage_format(self):
        '''Simple inequality storage format.

            >>> z(simple_inequality)
            timerelationtools.SimpleInequality('timespan_2.start < timespan_1.start')

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    @property
    def template(self):
        '''Simple inequality template.

            >>> simple_inequality.template
            'timespan_2.start < timespan_1.start'

        Return string.
        '''
        return self._template

    ### PUBLIC METHODS ###

    # TODO: to be implemented
