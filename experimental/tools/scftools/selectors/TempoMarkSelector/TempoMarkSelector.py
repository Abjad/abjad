from experimental.tools.scftools.selectors.Selector import Selector


class TempoMarkSelector(Selector):

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'tempo'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        current_score_package_proxy = self.session.current_score_package_proxy
        try:
            result.extend(current_score_package_proxy.tempo_inventory)
        except AttributeError:
            pass
        return result
