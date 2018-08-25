import copy
import typing
from abjad.system.LilyPondFormatManager import LilyPondFormatManager
from abjad.utilities.String import String
from .LilyPondNameManager import LilyPondNameManager


class LilyPondTweakManager(LilyPondNameManager):
    """
    LilyPond tweak manager.

    ..  container:: example

        Tweak managers are created by the ``abjad.tweak()`` factory function:

        >>> beam = abjad.Beam()
        >>> abjad.tweak(beam)
        LilyPondTweakManager()

        Set an attribute like this:

        >>> abjad.tweak(beam).color = 'red'

        The state of the tweak manager has changed:

        >>> abjad.tweak(beam)
        LilyPondTweakManager(('color', 'red'))

        And the value of the attribute just set is available like this:

        >>> abjad.tweak(beam).color
        'red'

        Trying to get an attribute that has not yet been set raises an
        attribute error:

        >>> abjad.tweak(beam).foo
        Traceback (most recent call last):
            ...
        AttributeError: LilyPondTweakManager object has no attribute 'foo'.
        
    """

    ### INITIALIZER ###

    def __init__(
        self,
        deactivate: bool = None,
        tag: str = None,
        ) -> None:
        if deactivate is not None:
            self._currently_deactivated = deactivate
        if tag is not None:
            self._currently_tagging = tag

    ### SPECIAL METHODS ###

    def __getattr__(self, name) -> typing.Union[
        LilyPondNameManager, typing.Any,
        ]:
        r"""
        Gets LilyPondNameManager (or LilyPondGrobNameManager) keyed to 
        ``name``.

        ..  container:: example

            Getting a grob name returns a LilyPondNameManager:

            >>> hairpin = abjad.Hairpin('p < f')
            >>> abjad.tweak(hairpin).dynamic_line_spanner
            LilyPondNameManager()

            Set a tweak with explicit grob like this:

            >>> abjad.tweak(hairpin).dynamic_line_spanner.staff_padding = 5

            This changes tweak manager state:

            >>> abjad.tweak(hairpin)
            LilyPondTweakManager(('dynamic_line_spanner', LilyPondNameManager(('staff_padding', 5))))

            Grob is available like this:

            >>> abjad.tweak(hairpin).dynamic_line_spanner
            LilyPondNameManager(('staff_padding', 5))

            Attribute is available like this:

            >>> abjad.tweak(hairpin).dynamic_line_spanner.staff_padding
            5

            Grob-explicit tweak appears like this:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(hairpin, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP
            
            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'4
                    - \tweak DynamicLineSpanner.staff-padding #5
                    \<
                    \p
                    d'4
                    e'4
                    f'4
                    \f
                }

        ..  container:: example

            Tweaks may be tagged:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup('Allegro', direction=abjad.Up).italic()
            >>> abjad.tweak(markup, tag='+PARTS').color = 'red'
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                - \tweak color #red %! +PARTS
                ^ \markup {
                    \italic
                        Allegro
                    }
                d'4
                e'4
                f'4
            }

            Tweaks may be tagged with ``deactivate=True``:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup('Allegro', direction=abjad.Up).italic()
            >>> abjad.tweak(markup, deactivate=True, tag='+PARTS').color = 'red'
            >>> abjad.attach(markup, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
            %@% - \tweak color #red     %! +PARTS
                ^ \markup {
                    \italic
                        Allegro
                    }
                d'4
                e'4
                f'4
            }

            Tweak tags and indicator tags may be set together:

            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> markup = abjad.Markup('Allegro', direction=abjad.Up).italic()
            >>> abjad.tweak(markup, tag='+PARTS').color = 'red'
            >>> abjad.attach(markup, staff[0], tag='RED:M1')
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff, strict=40)
            \new Staff
            {
                c'4
                - \tweak color #red                 %! +PARTS
                ^ \markup {                         %! RED:M1
                    \italic                         %! RED:M1
                        Allegro                     %! RED:M1
                    }                               %! RED:M1
                d'4
                e'4
                f'4
            }

        ..  container:: example

            Tweak expressions work like this:

            >>> abjad.tweak('red').color
            LilyPondTweakManager(('color', 'red'))

            >>> abjad.tweak(6).Y_offset
            LilyPondTweakManager(('Y_offset', 6))

            >>> abjad.tweak(False).bound_details__left_broken__text
            LilyPondTweakManager(('bound_details__left_broken__text', False))

        """
        from abjad.ly import contexts
        from abjad.ly import grob_interfaces
        if name == '_currently_deactivated':
            return vars(self).get('_currently_deactivated')
        if name == '_currently_tagging':
            return vars(self).get('_currently_tagging')
        if '_pending_value' in vars(self):
            _pending_value = self._pending_value
            self.__setattr__(name, _pending_value)
            delattr(self, '_pending_value')
            return self
        camel_name = String(name).to_upper_camel_case()
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                type_name = type(self).__name__
                message = f'{type_name} object has no attribute {name!r}.'
                raise AttributeError(message)
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
                message = f'{type_name} object has no attribute {name!r}.'
                raise AttributeError(message)

    def __setattr__(self, name, value):
        """
        Sets attribute ``name`` equal to ``value``.

        ..  container:: example

            Allows LilyPond colors:

            >>> abjad.tweak('ForestGreen').color
            LilyPondTweakManager(('color', 'ForestGreen'))

            >>> string = "#(x11-color 'blue)"
            >>> abjad.tweak(string).color
            LilyPondTweakManager(('color', "#(x11-color 'blue)"))

            Raises exception on unknown color:

            >>> abjad.tweak('SavannahGreen').color
            Traceback (most recent call last):
                ...
            Exception: 'SavannahGreen' is not a LilyPond color.

        """
        from abjad.ly.colors import colors
        if name == 'color':
            if 'x11-color' in value:
                _, color = value.split()
                color = color.strip("'").strip(')')
            else:
                color = value
            if color not in colors:
                raise Exception(f'{repr(value)} is not a LilyPond color.')
        tag = getattr(self, '_currently_tagging', None)
        deactivate = getattr(self, '_currently_deactivated', None)
        if tag is not None:
            if deactivate is True:
                value = ('TAGGED', value, tag, True)
            else:
                value = ('TAGGED', value, tag)
        object.__setattr__(self, name, value)
        if name in ('_currently_deactivated', '_currently_tagging'):
            return
        try:
            delattr(self, '_currently_deactivated')
        except AttributeError:
            pass
        try:
            delattr(self, '_currently_tagging')
        except AttributeError:
            pass

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self) -> typing.List[typing.Tuple]:
        result: typing.List[typing.Tuple] = []
        for name, value in vars(self).items():
            if name == '_currently_tagging':
                continue
            if type(value) is LilyPondNameManager:
                grob_name = name
                grob_proxy = value
                pairs = iter(vars(grob_proxy).items())
                for attribute_name, attribute_value in pairs:
                    triple = (grob_name, attribute_name, attribute_value)
                    result.append(triple)
            else:
                attribute_name = name
                attribute_value = value
                pair = (attribute_name, attribute_value)
                result.append(pair)
        return result

    def _list_format_contributions(self, directed=True):
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 2:
                grob = None
                attribute = attribute_tuple[0]
                value = attribute_tuple[1]
            elif len(attribute_tuple) == 3:
                grob = attribute_tuple[0]
                attribute = attribute_tuple[1]
                value = attribute_tuple[2]
            else:
                message = f'invalid attribute tuple: {attribute_tuple!r}.'
                raise ValueError(message)
            deactivate = False
            if isinstance(value, tuple) and value[0] == 'TAGGED':
                if len(value) == 4:
                    deactivate = value[3]
                tag = value[2]
                value = value[1]
            else:
                tag = None
            string = LilyPondFormatManager.make_lilypond_tweak_string(
                attribute,
                value,
                directed=directed,
                grob=grob,
                )
            if tag is not None:
                strings = [string]
                strings = LilyPondFormatManager.tag(
                    strings,
                    deactivate=deactivate,
                    tag=tag,
                    )
                string = strings[0]
            result.append(string)
        result.sort()
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def set_tweaks(
        argument,
        tweaks: typing.Union[
            typing.List[typing.Tuple],
            'LilyPondTweakManager',
            None,
            ],
        ) -> None:
        """
        Sets ``tweaks`` on ``argument``.
        """
        if not hasattr(argument, '_tweaks'):
            name = type(argument).__name__
            raise NotImplementedError(f'{name} does not allow tweaks (yet).')
        if not tweaks:
            return
        if isinstance(tweaks, LilyPondTweakManager):
            tweaks = tweaks._get_attribute_tuples()
        if not isinstance(tweaks, list):
            raise Exception(f'tweaks must be list of tuples (not {tweaks!r}).')
        assert all(isinstance(_, tuple) for _ in tweaks), repr(tweaks)
        if not tweaks:
            return
        if argument._tweaks is None:
            argument._tweaks = LilyPondTweakManager()
        manager = argument._tweaks
        for tweak in tweaks:
            if len(tweak) == 2:
                attribute, value = tweak
                value = copy.copy(value)
                setattr(manager, attribute, value)
            elif len(tweak) == 3:
                grob, attribute, value = tweak
                value = copy.copy(value)
                grob = getattr(manager, grob)
                setattr(grob, attribute, value)
            else:
                message = 'tweak tuple must have length 2 or 3'
                message += f' (not {tweak!r}).'
                raise ValueError(message)
