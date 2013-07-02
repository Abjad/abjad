from experimental.tools.scoremanagertools.selectors.Selector import Selector


class PerformerSelector(Selector):

    ### CLASS VARIABLES ###

    space_delimited_lowercase_target_name = 'performer'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        current_score_package_proxy = self.session.current_score_package_proxy
        try:
            result.extend(
                current_score_package_proxy.instrumentation.performers)
        except AttributeError:
            pass
        return result
