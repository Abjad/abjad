# -*- encoding: utf-8 -*-
import core
import editors
import exceptions
import getters
import iotools
import managers
import predicates
import wizards
import wranglers

'''Installing the Abjad score manager.

Do the following to install the score manager on your system:

    1. verify the score manager directories.
    2. add scoremanager/scr/ to your PATH for the start-score-manager script.
    3. create a user-specific scores/ directory.
    4. start and stop the score manager.
    5. run the score manager tools pytest battery.
    6. rebuild the Abjad score manager API.
    7. run doctest on the scoremanager/ directory.

1. Verify the score manager directories. The following 14 directories should 
appear on your filesystem after checkout:

    boilerplate/
    core/
    editors/
    etc/
    getters/
    iotools/
    latex/
    managers/
    materials/
    predicates/
    scores/
    scr/
    wizards/
    wranglers/

2. Add the scoremanager/scr/ directory to your PATH. This tells your shell 
where the start-score-manager script is housed:

    export PATH=$ABJAD/scoremanager/scr:$PATH

3. Create a scores directory. You can do this anywhere on your filesystem 
you wish. Then create a scores environment variable in your profile. Set the 
scores environment variable to your scores directory:

    export scores=$DOCUMENTS/scores

4. Start and stop the score manager. Type start-score-manager from the
commandline and the score manager should start. What you see here probably
won't be very interesting because you won't yet have any score manager scores
created on your system. But you should see three abjad example scores as
well as three or four menu options. The menu options will allow you to manage
materials, stylesheets and scores. If the shell can't find start-score-manager
then make sure you added the scroremanager/scr/ directory to your PATH. After
the score manager starts correctly enter 'q' to quit the score manager.

5. Run pytest against the scoremanager directory. Fix or report tests that
break.

6. Build the Abjad score manager API. Run 'avj api -S' to do this.

7. Run doctest on the scoremanager/ directory.  Run 'ajv doctest' in
scoremanager/ directory to do this. You're ready to use the score manager when
all tests pass.
'''
from abjad.tools import systemtools


systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'score manager'
