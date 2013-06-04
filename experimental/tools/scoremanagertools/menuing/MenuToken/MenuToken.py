from abjad.tools.abctools.AbjadObject import AbjadObject


class MenuToken(list, AbjadObject):
    '''Menu token.

    The tuple-only code indicates the following:

        * a value-tuple token has length 3
        * a prepopulated return value tuple token has length 4

    Return menu token.
    '''

    ### INITIALIZER ###

    def __init__(self, *args):
        assert 1 <= len(args) <= 4, repr(args)
        for arg in args:
            self.append(arg)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self._class_name, ', '.join([repr(x) for x in self]))

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def is_string_token(self):
        return len(self) == 1 and isinstance(self[0], str)

    @property
    def is_tuple_token(self):
        return not self.is_string_token
