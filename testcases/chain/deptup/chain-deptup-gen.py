import os
import shutil
from functools import partial

factnum = 1
outputfolder = '.\\'

for rulenum in range(0,501,50):
  tcfolder = 'chain-deptup{0:03d}-{1:d}'.format(rulenum, factnum)
  if os.path.exists(outputfolder + tcfolder):
    shutil.rmtree(outputfolder + tcfolder)
    
  os.makedirs(outputfolder + tcfolder)

  tcprefix = outputfolder + tcfolder + '\\' + tcfolder + '-'
  kb = open(tcprefix + 'KB.psoa', 'w')
  myprint = partial(print, file=kb, sep='')

  myprint('Document (')
  myprint('  Group (')
  for i in range(rulenum,0,-1):
      myprint('    Forall ?X1 ?X2 ?X3 (')
      myprint('      _r', i, '(?X1 ?X2 ?X3) :- _r', i-1, '(?X1 ?X2 ?X3)')
      myprint('    )')
      myprint()

  if factnum == 1:
    myprint('    _r0(_a1 _a2 _a3)')
  else:
    for i in range(1,factnum+1,1):
        myprint('    _r0(_a', i, '_1 _a', i, '_2 _a', i, '_3)')
      
  myprint('  )')
  myprint(')')
  kb.close()

  query1 = open(tcprefix + 'query1.psoa', 'w')
  print('_r', rulenum, '(?X1 ?X2 ?X3)', file=query1, sep='')
  query1.close()

  answer1path = tcprefix + 'answer1.psoa'
  answer1 = open(answer1path, 'w')
  if factnum == 1:
    print('?X1=_a1 ?X2=_a2 ?X3=_a3', file=answer1, sep='')
  else:
    for i in range(1,factnum+1,1):
      print('?X1=_a', i, '_1 ?X2=_a', i, '_2 ?X3=_a', i, '_3', file=answer1, sep='')
  answer1.close()

