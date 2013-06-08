from experimental.tools.newabjadbooktools.ImageOutputProxy import ImageOutputProxy


class GnuplotOutputProxy(ImageOutputProxy):
    '''Output proxy for Gnuplot images of Abjad datastructures:

    ::

        >>> bpf = datastructuretools.BreakPointFunction({
        ...     0.:   0.,  
        ...     0.75: (-1, 1.),
        ...     1.:   0.25,
        ...     })

    ::

        >>> output_proxy = newabjadbooktools.GnuplotOutputProxy(bpf)

    Return output proxy.
    '''

    ### CLASS VARIABLES ###

    def __init__(self, payload):
        if isinstance(payload, str):
            self._payload = payload
        else:
            gnuplot_format = payload.gnuplot_format
            self._payload = gnuplot_format
             
