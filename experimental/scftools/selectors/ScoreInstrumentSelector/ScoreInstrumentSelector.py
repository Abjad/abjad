from abjad.tools import instrumenttools
from scftools.selectors.Selector import Selector


class ScoreInstrumentSelector(Selector):

    ### CLASS ATTRIBUTES ###

    target_human_readable_name = 'instrument'

    ### PUBLIC METHODS ###

    def list_items(self):
        result = []
        if self.session.is_in_score:
            result.extend(self.session.current_score_package_proxy.instrumentation.instruments)
            result.append('other')
        return result
