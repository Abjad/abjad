from experimental.tools.handlertools.Handler import Handler


class PitchHandler(Handler):

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _tools_package_name(self):
        return 'handlertools.pitch'
