from abjad.tools.datastructuretools.ObjectInventory import ObjectInventory


class ExpressionInventory(ObjectInventory):
    '''Expression inventory.

    Each expression will be evaluated in turn.
    '''
    
    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        results = []
        for expression in self:
            result = expression._get_payload(score_specification)
            results.append(result)
        return results
