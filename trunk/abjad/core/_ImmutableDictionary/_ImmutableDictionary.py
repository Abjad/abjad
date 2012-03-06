from abjad.core._ImmutableAbjadObject import _ImmutableAbjadObject


class _ImmutableDictionary(dict, _ImmutableAbjadObject):
    '''.. versionadded:: 2.0
    '''

    def __delitem__(self, *args):
        #raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)
        raise AttributeError('objects are immutable: "{}".'.format(self.class_name))

    def __setitem__(self, *args):
        #raise AttributeError('objects are immutable: "%s".' % self.__class__.__name__)
        raise AttributeError('objects are immutable: "{}".'.format(self.class_name))
