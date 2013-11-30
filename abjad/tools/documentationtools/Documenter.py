# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools.abctools.AbjadObject import AbjadObject


class Documenter(AbjadObject):
    r'''Documenter is an abstract base class for documentation classes.
    '''

    ### INITIALIZER ###

    def __init__(self, obj, prefix='abjad.tools.'):
        assert isinstance(prefix, (str, type(None)))
        self._object = obj
        self._prefix = prefix

    ### SPECIAL METHODS ###

    @property
    def __format__(self, format_specification=''):
        r'''Formats documenter.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __makenew__(self, obj=None, prefix=None):
        obj = obj or self.obj
        prefix = prefix or self.prefix
        return type(self)(obj=obj, prefix=prefix)

    ### PRIVATE METHODS ###

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
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=(self._object,),
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def write(file_path, restructured_text):
        should_write = True
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                if f.read() == restructured_text:
                    should_write = False
        if should_write:
            print 'WRITING {}'.format(os.path.relpath(file_path))
            with open(file_path, 'w') as f:
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
