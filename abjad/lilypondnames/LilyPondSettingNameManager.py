import typing

from ..ly.contexts import contexts
from ..utilities.String import String
from .LilyPondNameManager import LilyPondNameManager


class LilyPondSettingNameManager(LilyPondNameManager):
    """
    LilyPond setting name manager.

    ..  container:: example

        >>> note = abjad.Note("c'4")
        >>> abjad.setting(note)
        LilyPondSettingNameManager()

    """

    ### SPECIAL METHODS ###

    def __getattr__(self, name: str) -> typing.Any:
        r"""
        Gets arbitrary object keyed to ``name``.

        ..  container:: example

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.setting(staff).instrument_name = abjad.Markup('Vn. I')
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                \with
                {
                    instrumentName = \markup { "Vn. I" }
                }
                {
                    c'4
                    d'4
                    e'4
                    f'4
                }

        ..  container:: example

            Returns arbitrary object keyed to ``name``:

            >>> abjad.setting(staff).instrument_name
            Markup(contents=['Vn. I'])

        """
        camel_name = String(name).to_upper_camel_case()
        if name.startswith("_"):
            try:
                return vars(self)[name]
            except KeyError:
                message = "{type(self).__name__!r} object has no attribute: {name!r}."
                raise AttributeError(message)
        elif camel_name in contexts:
            try:
                return vars(self)["_" + name]
            except KeyError:
                context = LilyPondNameManager()
                vars(self)["_" + name] = context
                return context
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = "{type(self).__name__!r} object has no attribute: {name!r}."
                raise AttributeError(message)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        result = []
        for name, value in vars(self).items():
            if type(value) is LilyPondNameManager:
                prefixed_context_name = name
                lilypond_type = prefixed_context_name.strip("_")
                context_proxy = value
                attribute_pairs = context_proxy._get_attribute_pairs()
                for attribute_name, attribute_value in attribute_pairs:
                    triple = (lilypond_type, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name, attribute_value = name, value
                result.append((attribute_name, attribute_value))
        return result


### FUNCTIONS ###


def setting(argument):
    r"""
    Makes LilyPond setting name manager.

    ..  container:: example

        Sets instrument name:

        >>> staff = abjad.Staff("c'4 e'4 d'4 f'4")
        >>> abjad.setting(staff).instrument_name = abjad.Markup('Vn. I')
        >>> abjad.show(staff) # doctest: +SKIP


        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            \with
            {
                instrumentName = \markup { "Vn. I" }
            }
            {
                c'4
                e'4
                d'4
                f'4
            }

    ..  container:: example

        Returns LilyPond setting name manager:

        >>> abjad.setting(staff)
        LilyPondSettingNameManager(('instrument_name', Markup(contents=['Vn. I'])))

    """
    if getattr(argument, "_lilypond_setting_name_manager", None) is None:
        manager = LilyPondSettingNameManager()
        argument._lilypond_setting_name_manager = manager
    return argument._lilypond_setting_name_manager
