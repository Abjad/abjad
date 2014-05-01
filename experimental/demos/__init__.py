# -*- encoding: utf-8 -*-
import sys
if sys.version_info[0] == 2:
    import bach
    import presentation
    import windungen
else:
    from experimental.demos import bach
    from experimental.demos import presentation
    from experimental.demos import windungen
del sys
