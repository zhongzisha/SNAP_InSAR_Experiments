

import sys,os,glob
import subprocess
import time


src_dir = r'G:\gdSAR'  # sys.argv[1]   # slaves
dst_dir = r'E:\step1_results'  # sys.argv[2]

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

SNAP_ROOT = r'E:\SNAP\snap-engine-9.0.0-SNAPSHOT'
SNAP_MAIN_EXE = r'java -cp "%s\modules\*;%s\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%s" ' \
                r'-Djava.library.path="%s\lib" -Xmx12G org.esa.snap.runtime.Launcher' % \
                (SNAP_ROOT, SNAP_ROOT, SNAP_ROOT, SNAP_ROOT)
print(SNAP_MAIN_EXE)

filenames = glob.glob(os.path.join(src_dir, 'S1A_*'))

for k, filename in enumerate(filenames):
    head, tail = os.path.split(filename)
    print(tail[17:25])
    command = r'%s step1_Split_and_ApplyOrbit_noDeburst.xml -Pinput1=%s -Poutput1=%s\%s.dim' % \
              (SNAP_MAIN_EXE, filename, dst_dir, tail[17:25])
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    print('SNAP STDOUT:{}'.format(stdout))
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('[' + str(k) + '] Finished process in ' + str(timeDelta) + ' seconds.')
    if process.returncode != 0:
        message = 'Error splitting slave ' + str(filename)
    else:
        message = 'Split slave ' + str(filename) + ' successfully completed.\n'
        print(message)

























