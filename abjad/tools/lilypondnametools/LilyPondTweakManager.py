# -*- coding: utf-8 -*-
from abjad.tools.lilypondnametools.LilyPondNameManager \
    import LilyPondNameManager


class LilyPondTweakManager(LilyPondNameManager):
    '''LilyPond tweak manager.
    '''

    ### PRIVATE METHODS ###

    def _list_format_contributions(self):
        from abjad.tools import systemtools
        manager = systemtools.LilyPondFormatManager
        result = []
        for attribute_pair in self._get_attribute_pairs():
            assert len(attribute_pair) == 2, repr(attribute_pair)
            attribute_name, attribute_value = attribute_pair
            string = manager.make_lilypond_tweak_string(
                attribute_name,
                attribute_value,
                )
            result.append(string)
        result.sort()
        return result
