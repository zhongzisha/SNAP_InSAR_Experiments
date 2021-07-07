import shutil
import sys ,os ,glob
import subprocess
import time
import numpy as np
from natsort import natsorted

src_dir = r'E:\step1_results'  # sys.argv[2]
dst_dir = r'D:\step2_results'  # sys.argv[2]
stamps_export_dir = r'D:\outputs_stamps'

if not os.path.exists(r'%s\result.txt' % src_dir):
    sys.exit(-1)

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)

SNAP_ROOT = r'E:\SNAP\snap-engine-9.0.0-SNAPSHOT'
SNAP_MAIN_EXE = r'java -cp "%s\modules\*;%s\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%s" ' \
                r'-Djava.library.path="%s\lib" -Xmx12G org.esa.snap.runtime.Launcher' % \
                (SNAP_ROOT, SNAP_ROOT, SNAP_ROOT, SNAP_ROOT)
print(SNAP_MAIN_EXE)

with open(r'%s\result.txt ' %src_dir) as fp:
    mst_prefix, width, height = fp.readline().strip().split(',')
    width = int(width)
    height = int(height)

filenames = natsorted(glob.glob(os.path.join(src_dir, '*.dim')))
print(filenames)

prefixes = set([f.split(os.sep)[-1].replace('.dim' ,'') for f in filenames])

slaves = natsorted(list(prefixes - {mst_prefix}))
print(slaves)

num_items_per_stack = 5

subset_width = 5120
subset_height = 5120

num_stacks = int(np.ceil(len(slaves) / num_items_per_stack))

remove_temporary_files = False

for ni in range(num_stacks):
    invalid_files = []
    items = [mst_prefix]
    for i in range(ni * num_items_per_stack, (ni + 1) * num_items_per_stack):
        if i < len(slaves):
            items.append(slaves[i])
    print(ni, items)

    input1 = ','.join([os.path.join(src_dir, item + '.dim') for item in items])
    output1 = os.path.join(dst_dir, '%s_Stack%d.dim'%(mst_prefix, ni))
    command = r'%s step3_Back_Geocoding.xml -Pinput1=%s -Poutput1=%s' % \
              (SNAP_MAIN_EXE, input1, output1)
    print(command)
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))

    # deburst: gpt.bat TOPSAR-Deburst -PselectedPolarisations=VV -Ssource="D:\step2_results\20200413_Stack0.dim" -t
    # D:\step2_results\20200413_Stack0_deb.dim
    input1 = output1
    output1 = input1.replace('.dim', '_deb.dim')
    command = r'%s TOPSAR-Deburst -PselectedPolarisations=VV -Ssource=%s -t %s' % \
              (SNAP_MAIN_EXE, input1, output1)
    print(command)
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))
    invalid_files.append(input1)
    invalid_files.append(input1.replace('.dim','.data'))

    # subset: gpt.bat Subset -Ssource="D:\outputs\20200413_Stack0_deb.dim" -Pregion=12786,6777,5120,
    # 5120 -PcopyMetadata=true -t D:\outputs\20200413_Stack0_deb_subset.dim
    input1 = output1
    output1 = input1.replace('.dim', '_sub.dim')
    command = r'%s Subset -Ssource=%s -Pregion=%d,%d,%d,%d -PcopyMetadata=true -t %s' % \
              (SNAP_MAIN_EXE, input1, width//2, height//2, subset_width, subset_height, output1)
    print(command)
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))
    invalid_files.append(input1)
    invalid_files.append(input1.replace('.dim','.data'))

    # do intererogram: gpt.bat Interferogram -p G:\gdSAR\snap_exps\interferogram_params.xml -SsourceProduct=%s -t %s
    input1 = output1
    output1 = input1.replace('.dim', '_ifg.dim')
    command = r'%s Interferogram -p interferogram_params.xml -SsourceProduct=%s -t %s' % \
              (SNAP_MAIN_EXE, input1, output1)
    print(command)
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))

    # delete the temporary files
    if remove_temporary_files:
        for item in invalid_files:
            shutil.rmtree(item, ignore_errors=True)

    # do stampsExport: gpt.bat G:\gdSAR\snap_exps\stampsExportGraph.xml
    # -Pinput1="D:\step2_results\20200413_Stack0_deb_subset.dim,D:\step2_results\20200413_Stack0_deb_subset_ifg.dim"
    # -Poutput1="E:\outputs_stamps"
    input1 = ','.join([input1, output1])
    output1 = stamps_export_dir
    command = r'%s stampsExportGraph.xml -Pinput1=%s -Poutput1=%s' % \
              (SNAP_MAIN_EXE, input1, output1)
    print(command)
    # launching the process
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    timeStarted = time.time()
    stdout = process.communicate()[0]
    timeDelta = time.time() - timeStarted  # Get execution time.
    print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))

    import pdb
    pdb.set_trace()