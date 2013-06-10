from experimental.tools.newabjadbooktools.OutputProxy import OutputProxy


class CodeOutputProxy(OutputProxy):

    ### INITIALIZER ###

    def __init__(self, payload):
        self._payload = tuple(payload)
    
    ### READ-ONLY PRIVATE ATTRIBUTES ###

    @property
    def _contents_repr_string(self):
        result = ''
        if len(self.payload):
            result = '(\n'
            for x in self._payload:
                result += '\t{!r},\n'.format(x)
            result += '\t)'
        return result



