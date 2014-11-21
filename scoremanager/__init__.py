# -*- encoding: utf-8 -*-
'''Installing the Abjad IDE.

To install the Abjad IDE:

    1. verify the Abjad IDE directories.
    2. add scoremanager/scr/ to your PATH.
    3. create a scores/ directory.
    4. start and stop the Abjad IDE.
    5. run pytest.
    6. build the Abjad IDE API.
    7. run doctest.

1. Verify the Abjad IDE directories. The following 7 directories should appear
on your filesystem after checkout:

    boilerplate/
    docs/
    etc/
    idetools/
    scores/
    scr/
    test/

2. Add the scoremanager/scr/ directory to your PATH. This tells your shell
where the start-abjad-idetools script is housed:

    export PATH=$ABJAD/scoremanager/scr:$PATH

3. Create a scores directory. You can do this anywhere on your filesystem you
wish. Then create a SCORES environment variable in your profile. Set the scores
environment variable to your scores directory:

    export SCORES=$DOCUMENTS/scores

4. Start and stop the Abjad IDE. Type start-abjad-idetools at the commandline.
The Abjad IDE should start. What you see here probably won't be very
interesting because you won't yet have any scores created on your system. But
you should see three Abjad example scores as well as three or four menu
options. The menu options allow you to manage scores, segments, materials and
other assets. If the shell can't find start-abjad-idetools then make sure you
added the scroremanager/scr/ directory to your PATH. After the Abjad IDE starts
correctly enter 'q' to quit the Abjad IDE.

5. Run pytest against the scoremanager directory. Fix or report tests that
break.

6. Build the Abjad IDE API. Run 'avj api -S' to do this.

7. Run doctest on the scoremanager/ directory.  Run 'ajv doctest' in
scoremanager/ directory to do this. You're ready to use the Abjad IDE when
all tests pass.
'''
import sys
if sys.version_info[0] == 2:
    import idetools
else:
    from scoremanager import idetools
configuration = idetools.Configuration()
sys.path.insert(0, configuration.example_score_packages_directory)
del configuration
del sys