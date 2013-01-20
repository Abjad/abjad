import copy
from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory
from experimental.tools.settingtools.Expression import Expression


class ExpressionInventory(ObjectInventory, Expression):
    '''Expression inventory.

    Each expression will be evaluated in turn.
    '''
    
    ### SPECIAL METHODS ###

    def __deepcopy__(self, memo):
        tokens = [copy.deepcopy(x) for x in self]
        result = type(self)(tokens=tokens, name=self.name)
        return result

    ### PRIVATE METHODS ###

    def _evaluate(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        results = []
        for expression in self:
            result = expression._evaluate(score_specification, voice_name)
            results.append(result)
        return results
