from abjad.tools.spannertools.TextSpanner._TextSpannerFormatInterface import _TextSpannerFormatInterface


class _BracketSpannerFormatInterface(_TextSpannerFormatInterface):

    def __init__(self, spanner):
        _TextSpannerFormatInterface.__init__(self, spanner)
