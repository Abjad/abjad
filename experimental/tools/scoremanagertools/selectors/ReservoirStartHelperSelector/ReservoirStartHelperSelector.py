# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ReservoirStartHelperSelector(Selector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'reservoir start helper'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        result.append('start at index 0')
        result.append('start at index n')
        result.append('start at next unused index')
        return result
