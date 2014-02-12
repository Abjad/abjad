# -*- encoding: utf-8 -*-
import core
import editors
import exceptions
import getters
import iotools
import managers
import materialpackagemakers
import predicates
import specifiers
import wizards
import wranglers

'''Installing the Abjad score manager.

Do the following to install the score manager on your system:

    1. verify the score manager directories
    2. add abjad/experimental/scr to your PATH for the 
       start-score-manager script
    3. create a user-specific scores directory to house scores you will 
       make with the score manager
    4. start and stop the score manager
    5. run the score manager tools pytest battery
    6. rebuild the Abjad experimental API
    7. run doctest on the experimental branch of the repository

1. Verify the score manager directories.
The following six directories should appear on your filesystem 
after checkout:

    abjad/experimental/materials
    abjad/experimental/scm
    abjad/experimental/scr
    abjad/experimental/specifiers

2. Add the abjad/experimental/scr directory to your PATH.
This tells your shell where the start-score-manager script is housed:

    export PATH=$ABJADEXPERIMENTAL/scr:$PATH

3. Create a scores directory.
You can do this anywhere on your filesystem you wish.
Then create a scores environment variable in your profile.
Set the scores environment variable to your scores directory:

    export scores=$DOCUMENTS/scores

4. Start and stop the score manager.
Type start-score-manager from the commandline and the score manager 
should start.
What you see here probably won't be very interesting because you
won't yet have any score manager scores created on your system.
But you should see an empty list of scores as well as three or four 
menu options.
The menu options will allow you to manage materials and specifiers.
There will also be a menu option to create a new score.
If the shell can't find start-score-manager then make sure you added 
the abjad/experimental/scr directory to your PATH.
After score manager tools starts correctly enter 'q' to quit the 
score manager.

5. Run pytest against the scoremanagertools directory.
Fix or report tests that break.

6. Rebuild the Abjad experimental API.
Run 'avj api -X' to do this.

7. Run doctest on the experimental branch of the repository.
Run 'ajv doctest' in abjad/experimental to do this.
You're ready to use the score manager when everything passes.
'''
from abjad.tools import systemtools

systemtools.ImportManager.import_structured_package(
	__path__[0],
	globals(),
	)

_documentation_section = 'unstable'
