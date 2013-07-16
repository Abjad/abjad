import abc
import os
from abjad.tools import abctools


class Documenter(abctools.Maker):
    '''Documenter is an abstract base class for documentation classes.
    '''

    ### INITIALIZER ###

    def __init__(self, obj, prefix='abjad.tools.'):
        assert isinstance(prefix, (str, type(None)))
        self._object = obj
        self._prefix = prefix

    ### PRIVATE METHOD ###

    def _shrink_module_name(self, module):
        if self.prefix and module.startswith(self.prefix):
            module = module.partition(self.prefix)[-1]
        parts = module.split('.')
        unique = [parts[0]]
        for part in parts[1:]:
            if part != unique[-1]:
                unique.append(part)
        return '.'.join(unique)

    ### PRIVATE PROPERTIES ###
    
    @property
    def _positional_argument_names(self):
        return ('_object',)

    ### PUBLIC METHODS ###

    def new(self, obj=None, prefix=None):
        obj = obj or self.obj
        prefix = prefix or self.prefix
        return type(self)(obj=obj, prefix=prefix)

    @staticmethod
    def write(filepath, restructured_text):
        should_write = True
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                if f.read() == restructured_text:
                    should_write = False
        if should_write:
            print 'WRITING {}'.format(os.path.relpath(filepath))
            with open(filepath, 'w') as f:
                f.write(restructured_text)

    ### PUBLIC PROPERTIES ###

    @property
    def module_name(self):
        return '{}.{}'.format(self._object.__module__, self._object.__name__)

    @property
    def object(self):
        return self._object

    @property
    def prefix(self):
        return self._prefix

