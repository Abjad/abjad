# -*- encoding: utf-8 -*-
import code


class AbjadBookConsole(code.InteractiveConsole):

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
        locals['__name__'] = '__main__'
        locals['__package__'] = None
        code.InteractiveConsole.__init__(
            self,
            locals=locals,
            filename=filename,
            )
        self.document_handler = document_handler
        self.save_topleveltools_dict()

    ### PUBLIC METHODS ###

    def showsyntaxerror(self, filename=None):
        code.InteractiveConsole.showsyntaxerror(self, filename=filename)
        self.document_handler.register_error()

    def showtraceback(self):
        code.InteractiveConsole.showtraceback(self)
        self.document_handler.register_error()

    def unregister_error(self):
        if self.document_handler:
            self.document_handler.unregister_error()

    def save_topleveltools_dict(self):
        topleveltools = self.locals['topleveltools']
        self.cached_topleveltools_dict = topleveltools.__dict__.copy()

    def restore_topleveltools_dict(self):
        topleveltools = self.locals['topleveltools']
        topleveltools.__dict__.update(self.cached_topleveltools_dict)

    ### PUBLIC PROPERTIES ###

    @property
    def errored(self):
        if self.document_handler:
            return self.document_handler.errored
        return False