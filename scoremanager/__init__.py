# -*- encoding: utf-8 -*-
'''Installing the Abjad IDE.

Do the following to install the Abjad IDE on your system:

    1. verify the Abjad IDE directories.
    2. add scoremanager/scr/ to your PATH for the start-abjad-ide script.
    3. create a user-specific scores/ directory.
    4. start and stop the Abjad IDE.
    5. run pytest.
    6. build the Abjad IDE API.
    7. run doctest.

1. Verify the Abjad IDE directories. The following 11 directories should
appear on your filesystem after checkout:

    boilerplate/
    core/
    docs/
    etc/
    iotools/
    materials/
    predicates/
    scores/
    scr/
    test/
    wranglers/

2. Add the scoremanager/scr/ directory to your PATH. This tells your shell
where the start-abjad-ide script is housed:

    export PATH=$ABJAD/scoremanager/scr:$PATH

3. Create a scores directory. You can do this anywhere on your filesystem
you wish. Then create a SCORES environment variable in your profile. Set the
scores environment variable to your scores directory:

    export SCORES=$DOCUMENTS/scores

4. Start and stop the Abjad IDE. Type start-abjad-ide from the commandline and
the Abjad IDE should start. What you see here probably won't be very
interesting because you won't yet have any scores created on your system. But
you should see three Abjad example scores as well as three or four menu
options. The menu options will allow you to manage materials, stylesheets,
scores and other assets. If the shell can't find start-abjad-ide then make
sure you added the scroremanager/scr/ directory to your PATH. After the Abjad
IDE starts correctly enter 'q' to quit the Abjad IDE.

5. Run pytest against the scoremanager directory. Fix or report tests that
break.

6. Build the Abjad IDE API. Run 'avj api -S' to do this.

7. Run doctest on the scoremanager/ directory.  Run 'ajv doctest' in
scoremanager/ directory to do this. You're ready to use the Abjad IDE when
all tests pass.
'''
import sys
if sys.version_info[0] == 2:
    import core
    import exceptions
    import iotools
    import predicates
    import wranglers
else:
    from scoremanager import core
    from scoremanager import iotools
    from scoremanager import predicates
    from scoremanager import wranglers
del sys