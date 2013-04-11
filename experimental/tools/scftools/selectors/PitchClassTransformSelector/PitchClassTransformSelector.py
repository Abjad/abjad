from experimental.tools.scftools.selectors.Selector import Selector


class PitchClassTransformSelector(Selector):

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'pitch-class transform'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        result.append('transpose')
        result.append('invert')
        result.append('multiply')
        return result
