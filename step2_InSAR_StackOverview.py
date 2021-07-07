

import sys,os,glob
import subprocess
import time

src_dir = r'E:\step1_results'  # sys.argv[2]
dst_dir = r'E:\step1_results'  # sys.argv[2]

if os.path.exists(r'%s\result.txt' % dst_dir):
    sys.exit(-1)

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

SNAP_ROOT = r'E:\SNAP\snap-engine-9.0.0-SNAPSHOT'
INSAR_SO_PATH = r'E:\SNAP\DoInSARStackOverview\out\artifacts\DoInSARStackOverview_jar\DoInSARStackOverview.jar'
command = r'java -jar %s %s\fileList.txt %s\result.txt' % \
                (INSAR_SO_PATH, src_dir, dst_dir)
print(command)

filenames = glob.glob(os.path.join(src_dir, '*.dim'))

if len(filenames) > 0 and not os.path.exists(r'%s\fileList.txt' % src_dir):
    filenames = [f+'\n' for f in filenames]
    with open(r'%s\fileList.txt' % src_dir, 'w') as fp:
        fp.writelines(filenames)

# launching the process
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
timeStarted = time.time()
stdout = process.communicate()[0]
print('SNAP STDOUT:{}'.format(stdout))
timeDelta = time.time() - timeStarted  # Get execution time.























