import shutil
import sys, os, glob
import subprocess
import time
import numpy as np
from natsort import natsorted

src_dir = r'E:\step1_results'  # sys.argv[2]
dst_dir = r'D:\step2_results'  # sys.argv[2]
stamps_export_dir = r'D:\outputs_stamps'
stamps_run_dir = r'E:\stamps_runs_1'
drive_maps = {'D:\\': '/mnt/d/',
              'E:\\': '/mnt/e/'}

if not os.path.exists(r'%s\result.txt' % src_dir):
    sys.exit(-1)

if not os.path.exists(dst_dir):
    os.makedirs(dst_dir)
if not os.path.exists(stamps_run_dir):
    os.makedirs(stamps_run_dir)

matlab_tepmlate = """
ADO_PS=0.4;
NPatchesRange=5;
NPatchesAzimuth=5;
density_rand=1;
weed_standard_dev=0.6;
weed_time_win=365;
merge_resample_size=100;
unwrap_grid_size=100;
unwrap_time_win=365;
masterdate='%s';
cmd=['mt_prep_snap ' masterdate ' ' pwd '/Export ' num2str(ADO_PS) ' ' num2str(NPatchesRange) ' ' num2str(NPatchesAzimuth) ' 50 50'];
cmd
system(cmd);
stamps(1,1);
setparm('density_rand',density_rand);
setparm('weed_standard_dev',weed_standard_dev);
setparm('weed_time_win',weed_time_win);
setparm('merge_resample_size',merge_resample_size);
setparm('unwrap_grid_size',unwrap_grid_size);
setparm('unwrap_time_win',unwrap_grid_size);
stamps(2,5);
stamps(5,5); 

stamps(6,6);

ps_plot('u');savemyfigure('1_after_unwrapping.pdf');

stamps(7,7);
ps_plot('d');savemyfigure('2_DEM_error.pdf');
ps_plot('m');savemyfigure('3_master_atmosphere.pdf');
ps_plot('u-dm');savemyfigure('4_unwrapping_phase_subtract_errors.pdf');
ps_info;
ps_plot('w-dm');savemyfigure('5_unwrapping_phase_subtract_errors2.pdf');

setparm('scla_deramp','y');
stamps(7,7);

ps_plot('u-dmo');savemyfigure('6_unwrapping_phase_subtract_ramps.pdf');
ps_plot('u-o');savemyfigure('7_unwrapping_phase_subtract_any_errors.pdf');

ps_plot('v');savemyfigure('8_mean_velocity.pdf');
ps_plot('v-do');savemyfigure('9_mean_velocity_subtract_errors.pdf');
ps_plot('vs-do');savemyfigure('10_std_velocity_subtract_errors.pdf'); 

ps_plot('v-d');savemyfigure('11_std_velocity_subtract_dem_error.pdf'); 
ps_plot('v-d',-1);
load('ps_plot_v-d');
ps_gescatter('12_GoogleEarth.kml',ph_disp,1,0.4);

quit;
"""

SNAP_ROOT = r'E:\SNAP\snap-engine-9.0.0-SNAPSHOT'
SNAP_MAIN_EXE = r'java -cp "%s\modules\*;%s\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%s" ' \
                r'-Djava.library.path="%s\lib" -Xmx12G org.esa.snap.runtime.Launcher' % \
                (SNAP_ROOT, SNAP_ROOT, SNAP_ROOT, SNAP_ROOT)
print(SNAP_MAIN_EXE)

with open(r'%s\result.txt ' % src_dir) as fp:
    mst_prefix, width, height = fp.readline().strip().split(',')
    width = int(width)
    height = int(height)

filenames = natsorted(glob.glob(os.path.join(src_dir, '*.dim')))
print(filenames)

prefixes = set([f.split(os.sep)[-1].replace('.dim', '') for f in filenames])

slaves = natsorted(list(prefixes - {mst_prefix}))
print(slaves)

num_items_per_stack = 5

subset_width = 8192
subset_height = 8192

num_stacks = int(np.ceil(len(slaves) / num_items_per_stack))

remove_temporary_files = True

if True:
    for ni in range(num_stacks):
        invalid_files = []
        items = [mst_prefix]
        for i in range(ni * num_items_per_stack, (ni + 1) * num_items_per_stack):
            if i < len(slaves):
                items.append(slaves[i])
        print(ni, items)

        input1 = ','.join([os.path.join(src_dir, item + '.dim') for item in items])
        output1 = os.path.join(dst_dir, '%s_Stack%d.dim' % (mst_prefix, ni))
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
        invalid_files.append(input1.replace('.dim', '.data'))

        # subset: gpt.bat Subset -Ssource="D:\outputs\20200413_Stack0_deb.dim" -Pregion=12786,6777,5120,
        # 5120 -PcopyMetadata=true -t D:\outputs\20200413_Stack0_deb_subset.dim
        input1 = output1
        output1 = input1.replace('.dim', '_sub.dim')
        command = r'%s Subset -Ssource=%s -Pregion=%d,%d,%d,%d -PcopyMetadata=true -t %s' % \
                  (SNAP_MAIN_EXE, input1, width // 2, height // 2, subset_width, subset_height, output1)
        print(command)
        # launching the process
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        timeStarted = time.time()
        stdout = process.communicate()[0]
        timeDelta = time.time() - timeStarted  # Get execution time.
        print('SNAP STDOUT:{}, {}'.format(stdout, timeDelta))
        invalid_files.append(input1)
        invalid_files.append(input1.replace('.dim', '.data'))

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
                if os.path.isdir(item):
                    shutil.rmtree(item, ignore_errors=True)
                else:
                    os.remove(item)

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

        # import pdb
        # pdb.set_trace()

with open(r'%s/matlabscript.m' % stamps_run_dir, 'w') as fp:
    fp.write(matlab_tepmlate % mst_prefix)

with open(r'%s/run.bat' % stamps_run_dir, 'w') as fp:
    # fp.write('#!/bin/csh\n')
    # fp.write('cd %s\n' % (stamps_run_dir.replace('D:\\', drive_maps['D:\\']).replace('E:\\', drive_maps['E:\\'])))
    fp.write('bash -ic \"ln -sf %s ./Export\"\n' % (
        stamps_export_dir.replace('D:\\', drive_maps['D:\\']).replace('E:\\', drive_maps['E:\\'])))
    fp.write('bash -ic \"matlab -r \\\"run(\'matlabscript.m\');exit;\\\"\"')
