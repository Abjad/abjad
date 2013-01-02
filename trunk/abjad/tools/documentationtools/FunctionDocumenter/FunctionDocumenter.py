import types
from abjad.tools.documentationtools.Documenter import Documenter


class FunctionDocumenter(Documenter):
    '''FunctionDocumenter generates an ReST entry for a given function:

    ::

        >>> from abjad.tools.documentationtools import *

    ::

        >>> from abjad.tools.notetools import make_notes
        >>> documenter = FunctionDocumenter(make_notes)
        >>> print documenter()
        notetools.make_notes
        ====================
        <BLANKLINE>
        .. autofunction:: abjad.tools.notetools.make_notes.make_notes
           :noindex:

    Returns ``FunctionDocumenter``` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_object', '_prefix')

    ### INITIALIZER ###

    def __init__(self, obj, prefix='abjad.tools.'):
        assert isinstance(obj, types.FunctionType)
        if obj.__name__ == 'wrapper':
            obj = obj.func_closure[1].cell_contents
        Documenter.__init__(self, obj, prefix)

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Generate documentation.

        Returns string.
        '''
        from abjad.tools import documentationtools

        document = documentationtools.ReSTDocument()
        heading = documentationtools.ReSTHeading(
            level=2,
            text=self._shrink_module_name(self.object.__module__)
            )
        autodoc = documentationtools.ReSTAutodocDirective(
            argument=self.module_name,
            directive='autofunction',
            options={'noindex': True},
            )
        document.extend([heading, autodoc])

        return document.rest_format
