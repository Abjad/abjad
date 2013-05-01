from abjad.tools import instrumenttools
from experimental.tools.scoremanagertools.selectors.Selector import Selector


class ScoreInstrumentSelector(Selector):

    ### CLASS ATTRIBUTES ###

    space_delimited_lowercase_target_name = 'instrument'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        if self.session.is_in_score:
            result.extend(self.session.current_score_package_proxy.instrumentation.instruments)
            result.append('other')
        return result
