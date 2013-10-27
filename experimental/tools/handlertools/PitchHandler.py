# -*- encoding: utf-8 -*-
from experimental.tools.handlertools.Handler import Handler


class PitchHandler(Handler):

    ### PRIVATE PROPERTIES ###

    @property
    def _tools_package_name(self):
        return 'handlertools'
