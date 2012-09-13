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

    def __eq__(self, expr):
        if isinstance(expr, type(self)):
            if self.string == expr.string:
                return True
        return False

    def __call__(self, expr):
        return self.callback(expr)

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.string)

    ### PRIVATE METHODS ###

    # make special one-line storage format
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        return ['helpertools.{}({!r})'.format(self._class_name, self.string)]
