from abjad.tools.abctools.AbjadObject import AbjadObject


class Callback(AbjadObject):
    r'''.. versionadded:: 1.0

    Callback with string representation.
    '''

    ### INITIALIZER ###

    def __init__(self, callback, string):
        self.callback = callback
        self.string = string

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        return self.callback(expr)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.string)
