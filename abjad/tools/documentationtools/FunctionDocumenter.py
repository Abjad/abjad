# -*- encoding: utf-8 -*-
import types
from abjad.tools.documentationtools.Documenter import Documenter


class FunctionDocumenter(Documenter):
    r'''FunctionDocumenter generates an ReST entry for a given function:

    ::

        >>> documenter = documentationtools.FunctionDocumenter(scoretools.make_notes)
        >>> print documenter()
        scoretools.make_notes
        =====================
        <BLANKLINE>
        .. autofunction:: abjad.tools.scoretools.make_notes.make_notes
        <BLANKLINE>

    Returns ``FunctionDocumenter``` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, object_=None, prefix='abjad.tools.'):
        if isinstance(object_, types.FunctionType):
            if object_.__name__ == 'wrapper':
                object_ = object_.func_closure[1].cell_contents
        Documenter.__init__(self, object_, prefix)

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Generate documentation.

        Returns string.
        '''
        from abjad.tools import documentationtools
        document = documentationtools.ReSTDocument()
        stripped_function_name = self._shrink_module_name(
            self.object_.__module__)
        parts = self.object_.__module__.split('.')
        tools_package_path = '.'.join(parts[:3])
        tools_package_name, sep, function_name = \
            stripped_function_name.partition('.')
        banner = '{}.{}'.format(tools_package_name, function_name)
#        banner = ':py:mod:`{} <{}>`.{}'.format(
#            tools_package_name,
#            tools_package_path,
#            function_name,
#            )
        heading = documentationtools.ReSTHeading(
            level=2,
            text=banner,
            )
        autodoc = documentationtools.ReSTAutodocDirective(
            argument=self.module_name,
            directive='autofunction',
            options={
                },
            )
        document.extend([heading, autodoc])
        return document.rest_format
