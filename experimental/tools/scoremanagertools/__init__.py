# -*- encoding: utf-8 -*-
import editors
import exceptions
import getters
import helpers
import makers
import menuing
import music
import predicates
import proxies
import scoremanager
import selectors
import specifiers
import wizards
import wranglers

'''Installing the Abjad score manager.

Do the following to install the score manager on your system:

    1. verify the score manager directories
    2. add abjad/experimental/scr to your PATH for the start-score-manager script
    3. create a user-specific scores directory to house scores you will make with the score manager
    4. start and stop the score manager
    5. create Example Score I using the score manager
    6. create Example Score II using the score manager
    7. create Étude Score I using the score manager
    8. run the score manager tools py.test battery
    9. rebuild the Abjad experimental API
    10. run doctest on the experimental branch of the repository


1. Verify the score manager directories.
The following six directories should appear on your filesystem after checkout:

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
Type ...

    start-score-manager

... from the commandline and the score manager should start.
What you see here probably won't be very interesting because you
won't yet have any score manager scores created on your system.
But you should see an empty list of scores as well as three or four menu options.
The menu options will allow you to manage materials, specifiers and sketches.
There will also be a menu option to create a new score.
If the shell can't find start-score-manager then make sure you added 
the abjad/experimental/scr directory to your PATH.
After score manager tools starts correctly enter 'q' to quit the score manager.


5. Create Example Score I using score manager tools. 
Type 'start-score-manager' to start the score manager again.
Once the score manager starts you should see a menu item that says "new score (new)".
Type 'new'. You should then be presented with a 3-step score creation wizard.
Complete the wizard exactly as follows:

    (1/3) score title: Example Score I
    (2/3) package name: example_score_1
    (3/3) year of completion: 2013

Then set up instrumentation for Example Score I as follows:

    (1) hornist: horn
    (2) trombonist: tenor trombone
    (3) violinist: violin
    (4) cellist: cello
    (5) pianist: piano
    (6) percussionist: no instruments

Then add the tagline 'for six players'.

Then create a tempo inventory like this:

    'materials (m)'
    ... 
    'maker-maker (m)'
    ...
    'tempo mark inventory material package maker'

Give the material this name:

    Material name> tempo inventory

Then add the following four tempo marks:
    
    Tempo mark> (1, 8), 72
    Tempo mark> (1, 8), 108
    Tempo mark> (1, 8), 90
    Tempo mark> (1, 8), 135

Quit the score manager when you finish.
Check your scores directory.
You should see a example_score_1 directory.
List the contents of the example_score_1 score directory.
You should see the following:

    scores$ ls example_score_1/
    __init__.py dist        etc         exg         mus         tags.py


6. Create Example Score II using the score manager.
Repeat the steps listed for #5, above:

    (1/3) score title: Example Score II
    (2/3) package name: example_score_2
    (3/3) year of completion: 2013


7. Create Étude Score I using the score manager.
Repeat the steps listed above for #5 and #7.
Quit the score manager when your are done.
The score manager test battery runs against these three example scores.
    

8. Run py.test against the scoremanagertools directory.
Fix or report tests that break.


9. Rebuild the Abjad experimental API.
Run 'avj api -X' to do this.


10. Run doctest on the experimental branch of the repository.
Run 'ajv doctest' in abjad/experimental to do this.
You're ready to use the score manager when everything passes.
'''
from abjad.tools import importtools

importtools.import_structured_package(__path__[0], globals(), package_root_name='experimental')

_documentation_section = 'unstable'
