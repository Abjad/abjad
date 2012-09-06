import abc
from abjad.tools import abctools


class Documenter(abctools.AbjadObject):
    '''Documenter is an abstract base class for documentation classes.'''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = ('_object', '_prefix')

    ### INITIALIZER ###

    def __init__(self, obj, prefix='abjad.tools.'):
        assert isinstance(prefix, (str, type(None)))
        self._object = obj
        self._prefix = prefix

    ### SPECIAL METHODS ###

    def __call__(self):
        raise NotImplemented

    ### PRIVATE METHOD ###

    def _format_heading(self, text, character='='):
        return [text, character * len(text), '']

    def _shrink_module_name(self, module):
        if self.prefix and module.startswith(self.prefix):
            module = module.partition(self.prefix)[-1]
        parts = module.split('.')
        unique = [parts[0]]
        for part in parts[1:]:
            if part != unique[-1]:
                unique.append(part)
        return '.'.join(unique)

    ### PUBLIC PROPERTIES ###

    @property
    def module_name(self):
        return '%s.%s' % (self._object.__module__, self._object.__name__)

    @property
    def object(self):
        return self._object

    @property
    def prefix(self):
        return self._prefix
