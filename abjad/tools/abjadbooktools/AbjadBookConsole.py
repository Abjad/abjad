# -*- coding: utf-8 -*-
import code


class AbjadBookConsole(code.InteractiveConsole):
    r'''An interactive console which provides a sandboxed namespace for
    executing abjad-book code examples.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Internals'

    ### INITIALIZER ###

    def __init__(
        self,
        document_handler=None,
        locals=None,
        filename='<stdin>',
        ):
        import abjad
        if locals is None:
            locals = abjad.__dict__.copy()
        locals['__builtins__'] = __builtins__.copy()
        locals['__name__'] = '__main__'
        locals['__package__'] = None
        code.InteractiveConsole.__init__(
            self,
            locals=locals,
            filename=filename,
            )
        self.document_handler = document_handler
        self.save_topleveltools_dict()
        self.push('from __future__ import print_function')

    ### PUBLIC METHODS ###

    def restore_topleveltools_dict(self):
        r'''Restores the topleveltols module dictionary.
        '''
        topleveltools = self.locals['topleveltools']
        topleveltools.__dict__.update(self.cached_topleveltools_dict)

    def save_topleveltools_dict(self):
        r'''Caches the dictionary of the topleveltools module.

        Because CodeBlock replaces various topleveltools function references
        with its own proxies, the originals must be cached so they can later be
        restored. Otherwise Sphinx's autodoc extension will discover the
        abjad-book function proxies and not the originals.
        '''
        topleveltools = self.locals['topleveltools']
        self.cached_topleveltools_dict = topleveltools.__dict__.copy()

    def showsyntaxerror(self, filename=None):
        r'''Proxies Python's InteractiveConsole.showsyntaxerror().
        '''
        code.InteractiveConsole.showsyntaxerror(self, filename=filename)
        self.document_handler.register_error()

    def showtraceback(self):
        r'''Proxies Python's InteractiveConsole.showtraceback().
        '''
        code.InteractiveConsole.showtraceback(self)
        self.document_handler.register_error()

    def unregister_error(self):
        r'''Unregisters the last error registered in the current document
        handler.

        This occurs when the interpreting code block permits errors to appear.
        '''
        if self.document_handler:
            self.document_handler.unregister_error()

    ### PUBLIC PROPERTIES ###

    @property
    def errored(self):
        r'''Is true if the last line executed by the console errored.
        '''
        if self.document_handler:
            return self.document_handler.errored
        return False
