from proceedings import Proceedings
import time
import random
import re
import glob
import os


id = {}

id['ICSE'] = 'citation.cfm?id=2568225'
id['ISSTA'] = 'citation.cfm?id=2610384'
id['FSE'] = 'citation.cfm?id=2635868'
id['ESEC'] = 'citation.cfm?id=2491411'
id['ESEM'] = 'citation.cfm?id=2652524'
id['ASE'] = 'citation.cfm?id=2642937'

def scrap(citation_id):
    time.sleep(random.randint(50, 90))
    proc = Proceedings(citation_id)
    proc.dump()
    print proc.title
    while proc.get_prev() is not None:
        time.sleep(random.randrange(40, 100))
        cite = re.findall('.*id=\d*', proc.get_prev())[0]
        proc = Proceedings(cite)
        proc.dump()
        print proc.title





cwd = os.getcwd()

for conference in id:
    if not os.path.exists(conference):
        try:
            os.makedirs(conference)
        except OSError:
            raise
    print 'collecting data of conference {0}'.format(conference)
    os.chdir(conference)
    scrap(id[conference])
    os.chdir(cwd)
    
