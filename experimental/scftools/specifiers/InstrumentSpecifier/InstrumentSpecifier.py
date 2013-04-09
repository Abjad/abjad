from scftools.specifiers.ParameterSpecifier import ParameterSpecifier


class InstrumentSpecifier(ParameterSpecifier):

    def __init__(self, description=None, instrument=None, name=None, source=None):
        ParameterSpecifier.__init__(self, description=description, name=name, source=source)
        self.instrument = instrument

    ### READ-ONLY PROPERTIES ###

    @property
    def one_line_menuing_summary(self):
        value = self.name or self.instrument.instrument_name
        return 'instrument: {}'.format(value)
