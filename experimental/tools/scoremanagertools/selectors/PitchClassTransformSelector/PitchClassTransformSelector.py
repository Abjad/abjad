# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class PitchClassTransformSelector(Selector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'pitch-class transform'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        result.append('transpose')
        result.append('invert')
        result.append('multiply')
        return result
