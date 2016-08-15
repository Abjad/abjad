# -*- coding: utf-8 -*-
import enum
from abjad.tools import stringtools


class Enumeration(enum.IntEnum):
    r'''An enumeration.

    ::

        >>> class Colors(datastructuretools.Enumeration):
        ...     RED = 1
        ...     BLUE = 2
        ...     LIGHT_GREEN = 3
        ...

    ::

        >>> color = Colors.RED
        >>> print(repr(color))
        Colors.RED

    ::

        >>> Colors.from_expr('light green')
        Colors.LIGHT_GREEN

    '''

    ### SPECIAL METHODS ###

    def __dir__(self):
        names = [
            '__class__',
            '__doc__',
            '__format__',
            '__members__',
            '__module__',
            '__repr__',
            '_repr_specification',
            '_storage_format_specification',
            'from_expr',
            ]
        names += self._member_names_
        names += [
            ]
        return sorted(names)

    def __format__(self, format_specification=''):
        r'''Formats enumeration.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of enumeration.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatAgent(self).get_repr_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            repr_text='{}.{}'.format(
                type(self).__name__,
                self.name,
                ),
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatAgent(self)
        return systemtools.StorageFormatSpecification(
            self,
            storage_format_text='{}.{}.{}'.format(
                agent.get_tools_package_name(),
                type(self).__name__,
                self.name,
                ),
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        r'''Convenience constructor for enumerations.

        Returns new enumeration item.
        '''
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.strip()
            expr = stringtools.to_snake_case(expr) 
            expr = expr.upper()
            return cls[expr]
        elif expr is None:
            return cls(0)
        message = 'Cannot instantiate {} from {}.'.format(cls.__name__, expr)
        raise ValueError(message)
