from abjad.exceptions import NonbinaryTimeSignatureSuppressionError
from abjad.exceptions import OverfullMeasureError
from abjad.exceptions import UnderfullMeasureError
from abjad.tools.containertools.Container._ContainerFormatter import _ContainerFormatter
from abjad.tools.measuretools.Measure._MeasureFormatterSlotsInterface import _MeasureFormatterSlotsInterface


class _MeasureFormatter(_ContainerFormatter):

    def __init__(self, client):
        _ContainerFormatter.__init__(self, client)
        self._slots = _MeasureFormatterSlotsInterface(self)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _contents(self):
        result = []
        client = self._client
        # the class name test here is exclude scaleDurations from Anonymous and Dynamic measures
        #if client.is_nonbinary and client.__class__.__name__ == 'Measure':
        if client.is_nonbinary and client.__class__.__name__ == 'Measure':
            result.append("\t\\scaleDurations #'(%s . %s) {" % (
                client.multiplier.numerator,
                client.multiplier.denominator))
            #result.extend( ['\t' + x for x in _MeasureFormatter._contents.fget(self)])
            result.extend( ['\t' + x for x in _ContainerFormatter._contents.fget(self)])
            result.append('\t}')
        else:
            #result.extend(_MeasureFormatter._contents.fget(self))
            result.extend(_ContainerFormatter._contents.fget(self))
        return result

    ### PUBLIC ATTRIBUTES ###

    @property
    def format(self):
        from abjad.tools import contexttools
        client = self._client
        effective_meter = contexttools.get_effective_time_signature(self._client)
        if effective_meter.is_nonbinary and effective_meter.suppress:
            raise NonbinaryTimeSignatureSuppressionError
        #if effective_meter.duration < client.preprolated_duration:
        if effective_meter.duration < client.preprolated_duration:
            raise OverfullMeasureError
        #if client.preprolated_duration < effective_meter.duration:
        if client.preprolated_duration < effective_meter.duration:
            raise UnderfullMeasureError
        return _ContainerFormatter.format.fget(self)

    @property
    def slots(self):
        return self._slots
