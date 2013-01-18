from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.settingtools.Expression import Expression


class ExpressionInventory(ObjectInventory, Expression):
    '''Expression inventory.

    Each expression will be evaluated in turn.
    '''
    
    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        results = []
        for expression in self:
            # TODO: eventually change to expression._evaluate(score_specification)
            result = expression._get_timespan(score_specification, voice_name)
            results.append(result)
        return results
