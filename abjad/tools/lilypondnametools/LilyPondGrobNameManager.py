# -*- coding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondGrobNameManager(LilyPondNameManager):
    '''LilyPond grob name manager.
    '''

    ### CLASS VARIABLES ###

    skeleton_string_prefix = 'override__'

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        r'''Gets attribute `name` from LilyPond grob name manager.

        Returns string.
        '''
        from abjad import ly
        from abjad.tools import lilypondnametools
        camel_name = stringtools.to_upper_camel_case(name)
        if name.startswith('_'):
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)
        elif camel_name in ly.contexts:
            try:
                return vars(self)['_' + name]
            except KeyError:
                context = lilypondnametools.LilyPondGrobNameManager()
                vars(self)['_' + name] = context
                return context
        elif camel_name in ly.grob_interfaces:
            try:
                return vars(self)[name]
            except KeyError:
                vars(self)[name] = lilypondnametools.LilyPondNameManager()
                return vars(self)[name]
        else:
            try:
                return vars(self)[name]
            except KeyError:
                message = '{!r} object has no attribute: {!r}.'
                message = message.format(type(self).__name__, name)
                raise AttributeError(message)

    def __setattr__(self, attribute_name, value):
        r'''Sets attribute `attribute_name` of grob name manager to `value`.

        Returns none.
        '''
        # make sure attribute name is valid grob name before setting value
        attribute_value = getattr(self, attribute_name)
        object.__setattr__(self, attribute_name, value)

    ### PRIVATE METHODS ###

    def _get_attribute_tuples(self):
        from abjad.tools import lilypondnametools
        result = []
        for name, value in vars(self).items():
            if type(value) is lilypondnametools.LilyPondNameManager:
                grob_name, grob_proxy = name, value
                pairs = iter(vars(grob_proxy).items())
                for attribute_name, attribute_value in pairs:
                    triple = (grob_name, attribute_name, attribute_value)
                    result.append(triple)
            else:
                context_name, context_proxy = name.strip('_'), value
                for grob_name, grob_proxy in vars(context_proxy).items():
                    pairs = iter(vars(grob_proxy).items())
                    for attribute_name, attribute_value in pairs:
                        quadruple = (
                            context_name,
                            grob_name,
                            attribute_name,
                            attribute_value,
                            )
                        result.append(quadruple)
        return tuple(result)

    def _get_skeleton_strings(self):
        skeleton_strings = []
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            attribute_name = '_tools_package_qualified_repr'
            value = getattr(value, attribute_name, repr(value))
            string = 'override__{}={}'.format(most, value)
            skeleton_strings.append(string)
        return tuple(skeleton_strings)

    def _list_format_contributions(self, contribution_type, is_once=False):
        from abjad.tools import systemtools
        manager = systemtools.LilyPondFormatManager
        assert contribution_type in ('override', 'revert')
        result = []
        for attribute_tuple in self._get_attribute_tuples():
            if len(attribute_tuple) == 3:
                context_name = None
                grob_name = attribute_tuple[0]
                attribute_name = attribute_tuple[1]
                attribute_value = attribute_tuple[2]
            elif len(attribute_tuple) == 4:
                context_name = attribute_tuple[0]
                grob_name = attribute_tuple[1]
                attribute_name = attribute_tuple[2]
                attribute_value = attribute_tuple[3]
            else:
                raise ValueError
            if contribution_type == 'override':
                override_string = manager.make_lilypond_override_string(
                    grob_name,
                    attribute_name,
                    attribute_value,
                    context_name=context_name,
                    is_once=is_once,
                    )
                result.append(override_string)
            else:
                revert_string = manager.make_lilypond_revert_string(
                    grob_name,
                    attribute_name,
                    context_name=context_name,
                    )
                result.append(revert_string)
        result.sort()
        return result

    def _make_override_dictionary(self):
        result = {}
        grob_override_tuples = self._get_attribute_tuples()
        for grob_override_tuple in grob_override_tuples:
            most = '__'.join(grob_override_tuple[:-1])
            value = grob_override_tuple[-1]
            attribute = '_tools_package_qualified_repr'
            value = getattr(value, attribute, repr(value))
            result[most] = value
        return result
