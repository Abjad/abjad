# -*- encoding: utf-8 -*-
import abc
import os
from abjad.tools.abctools.AbjadObject import AbjadObject


class Documenter(AbjadObject):
    r'''Documenter is an abstract base class for documentation classes.
    '''

    ### INITIALIZER ###

    def __init__(self, object_=None, prefix='abjad.tools.'):
        assert isinstance(prefix, (str, type(None)))
        self._object_ = object_
        self._prefix = prefix

    ### SPECIAL METHODS ###

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

    def __makenew__(self, object_=None, prefix=None):
        r'''Makes new documenter.

        Returns new documenter.
        '''
        object_ = object_ or self.object_
        prefix = prefix or self.prefix
        return type(self)(object_=object_, prefix=prefix)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        keyword_argument_names = (
            'prefix',
            )
        if self.object_ is type(None):
            positional_argument_values = ()
        else:
            positional_argument_values = (
                self.object_,
                )
        return systemtools.StorageFormatSpecification(
            self,
            positional_argument_values=positional_argument_values,
            keyword_argument_names=keyword_argument_names,
            )

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

    ### PUBLIC METHODS ###

    @staticmethod
    def write(file_path, restructured_text):
        r'''Writes `restructed_text` to `file_path`.

        Returns none.
        '''
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
        r'''Module name of documenter.

        Returns string.
        '''
        return '{}.{}'.format(self.object_.__module__, self.object_.__name__)

    @property
    def object_(self):
        r'''Object of documenter.
        '''
        return self._object_

    @property
    def prefix(self):
        r'''Prefix of documenter.
        '''
        return self._prefix
