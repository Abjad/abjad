from experimental.tools.newabjadbooktools.ImageOutputProxy import ImageOutputProxy


class GraphvizOutputProxy(ImageOutputProxy):

    ### CLASS VARIABLES ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            graphviz_format = payload.graphviz_format
            self._payload = graphviz_format
             
