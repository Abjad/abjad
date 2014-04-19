# -*- encoding: utf-8 -*-
import sys
if sys.version_info[0] == 2:
    import desordre
    import ferneyhough
    import mozart
    import part
else:
    from abjad.demos import desordre
    from abjad.demos import ferneyhough
    from abjad.demos import mozart
    from abjad.demos import part
del sys
