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
    
        


# def papers2json(directory, file_name):
#     outfile = open(file_name, 'w')
#     for f in glob.glob(directory + '*.json'):
#         print 'Processing', f
#         proc =Proceedings()
#         proc.load(f)
#         for l in proc.get_papers():
#             outfile.write(str(l) + '\n')
#     outfile.close()
#
# # papers2json(sys.argv[1], sys.argv[2])
# cwd = os.getcwd()
# os.chdir('icse')
# scrap(ICSE_ID)
# os.chdir(cwd + os.sep + 'fse')
# scrap(FSE_ID)
# os.chdir(cwd + os.sep + 'esec')
# scrap(ESEC_ID)
# os.chdir(cwd + os.sep + 'issta')
# scrap(ISSTA_ID)
# os.chdir(cwd + os.sep + 'ase')
# scrap(ASE_ID)
