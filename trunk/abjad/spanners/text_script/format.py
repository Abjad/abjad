from abjad.spanners.spanner.format import _SpannerFormatInterface


class _TextScriptSpannerFormatInterface(_SpannerFormatInterface):

   def __init__(self, spanner):
      _SpannerFormatInterface.__init__(self, spanner)
