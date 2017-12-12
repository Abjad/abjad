import enum


class Enumeration(enum.IntEnum):
    r'''Enumeration.

    ..  container:: example

        >>> class Colors(abjad.Enumeration):
        ...     RED = 1
        ...     BLUE = 2
        ...     LIGHT_GREEN = 3
        ...

        >>> color = Colors.RED
        >>> print(repr(color))
        Colors.RED

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
            '_get_format_specification',
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
            return systemtools.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __repr__(self):
        r'''Gets interpreter representation of enumeration.

        Returns string.
        '''
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad.tools import systemtools
        agent = systemtools.StorageFormatManager(self)
        repr_text = '{}.{}'.format(type(self).__name__, self.name)
        storage_format_text = '{}.{}'.format(
            agent.get_tools_package_name(),
            repr_text,
            )
        return systemtools.FormatSpecification(
            client=self,
            repr_text=repr_text,
            storage_format_text=storage_format_text,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, argument):
        r'''Convenience constructor for enumerations.

        Returns new enumeration item.
        '''
        from abjad.tools import datastructuretools
        if isinstance(argument, cls):
            return argument
        elif isinstance(argument, int):
            return cls(argument)
        elif isinstance(argument, str):
            argument = argument.strip()
            argument = datastructuretools.String(argument).to_snake_case()
            argument = argument.upper()
            try:
                return cls[argument]
            except KeyError:
                return cls[argument.replace('_', '')]
        elif argument is None:
            return cls(0)
        message = 'Cannot instantiate {} from {}.'.format(
            cls.__name__,
            argument,
            )
        raise ValueError(message)
