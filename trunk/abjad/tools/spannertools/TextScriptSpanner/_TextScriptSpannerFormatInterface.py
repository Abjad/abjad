from abjad.tools.spannertools.Spanner._SpannerFormatInterface import _SpannerFormatInterface


class _TextScriptSpannerFormatInterface(_SpannerFormatInterface):

    def __init__(self, spanner):
        _SpannerFormatInterface.__init__(self, spanner)
