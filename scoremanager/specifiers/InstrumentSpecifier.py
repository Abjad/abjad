# -*- encoding: utf-8 -*-
from scoremanager.specifiers.ParameterSpecifier import ParameterSpecifier


class InstrumentSpecifier(ParameterSpecifier):

    def __init__(
        self,
        description=None,
        instrument=None,
        custom_identifier=None,
        source=None,
        ):
        ParameterSpecifier.__init__(
            self,
            description=description,
            custom_identifier=custom_identifier,
            source=source,
            )
        self.instrument = instrument

    ### PRIVATE PROPERTIES ###

    @property
    def _one_line_menuing_summary(self):
        value = self.custom_identifier or self.instrument.instrument_name
        return 'instrument: {}'.format(value)
