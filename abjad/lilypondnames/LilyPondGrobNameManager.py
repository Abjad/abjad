import typing
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.utilities.String import String
from .LilyPondNameManager import LilyPondNameManager


class LilyPondGrobNameManager(LilyPondNameManager):
    """
    LilyPond grob name manager.

    ..  container:: example

        LilyPondGrobNameManager instances are created by the
        ``abjad.override()`` factory function:

        >>> note = abjad.Note("c'4")
        >>> abjad.override(note)
        LilyPondGrobNameManager()

    """

    ### SPECIAL METHODS ###

    def __getattr__(self, name) -> typing.Union[
        LilyPondNameManager, 'LilyPondGrobNameManager'
        ]:
        r"""
        Gets LilyPondNameManager (or LilyPondGrobNameManager) keyed to 
        ``name``.

        ..  container:: example

            Somewhat confusingly, getting a grob name returns a
            LilyPondNameManager:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).note_head
            LilyPondNameManager()

            While getting a context name returns a LilyPondGrobNameManager:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).staff
            LilyPondGrobNameManager()

            Which can then be deferenced to get a LilyPondNameManager:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.override(staff[0]).staff.note_head
            LilyPondNameManager()

        Note that the dot-chained user syntax is unproblematic. But the class
        of each manager returned in the chain is likely to be surprising at
        first encounter.
        """
        from abjad.ly import contexts
        from abjad.ly import grob_interfaces
        camel_name = String(name).to_upper_camel_case()
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                message = '{type_name!r} object has no attribute: {name!r}.'
                raise AttributeError(message)
        elif camel_name in contexts:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = LilyPondGrobNameManager()
                vars(self)['_' + name] = context
                return context
        elif camel_name in grob_interfaces:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = LilyPondNameManager()
                return vars(self)[name]
        else:
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                message = f'{type_name!r} object has no attribute: {name!r}.'
                raise AttributeError(message)

    def __setattr__(self, attribute, value) -> None:
        """
        Sets attribute ``attribute`` of grob name manager to ``value``.
        """
        # make sure attribute name is valid grob name before setting value
        object.__setattr__(self, attribute, value)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).items():
            if type(value) is LilyPondNameManager:
                grob, grob_proxy = name, value
                pairs = iter(vars(grob_proxy).items())
                for attribute, value in pairs:
                    triple = (grob, attribute, value)
                    result.append(triple)
            else:
                context, context_proxy = name.strip('_'), value
                for grob, grob_proxy in vars(context_proxy).items():
                    pairs = iter(vars(grob_proxy).items())
                    for attribute, value in pairs:
                        quadruple = (
                            context,
                            grob,
                            attribute,
                            value,
                            )
                        result.append(quadruple)
        return tuple(result)

    def _list_format_contributions(self, contribution_type, once=False):
        manager = LilyPondFormatManager
        assert contribution_type in ('override', 'revert')
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context = None
                grob = attribute_tuple[0]
                attribute = attribute_tuple[1]
                value = attribute_tuple[2]
            elif len(attribute_tuple) == 4:
                context = attribute_tuple[0]
                grob = attribute_tuple[1]
                attribute = attribute_tuple[2]
                value = attribute_tuple[3]
            else:
                message = 'invalid attribute tuple: {attribute_tuple!r}.'
                raise ValueError(message)
            if contribution_type == 'override':
                override_string = manager.make_lilypond_override_string(
                    grob,
                    attribute,
                    value,
                    context=context,
                    once=once,
                    )
                result.append(override_string)
            else:
                revert_string = manager.make_lilypond_revert_string(
                    grob,
                    attribute,
                    context=context,
                    )
                result.append(revert_string)
        result.sort()
        return result
