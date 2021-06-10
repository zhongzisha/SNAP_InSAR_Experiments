import sys, os, glob
print(os.environ['SNAP_ROOT'])
SNAP_ROOT = os.environ['SNAP_ROOT']
OUTPUT_DIR = os.environ['OUTPUT_DIR']
SNAP_MAIN_EXE = os.environ['SNAP_MAIN_EXE']
print(SNAP_ROOT)
print(OUTPUT_DIR)
print(SNAP_MAIN_EXE)

if sys.argv[1] == '0':

    filename = glob.glob('UnwPhase_ifg_*.snaphu.img')
    if len(filename) == 0:
        with open('snaphu.conf', 'r') as fp:
            lines = fp.readlines()
            
        cmd = None
        for line in lines: 
            if 'snaphu -f' in line:
                cmd = line.replace('#', '')
                break
                
        if cmd is not None:
            print(cmd)
            os.system(cmd)

    filename = glob.glob('UnwPhase_ifg_*.snaphu.hdr')
    if len(filename) > 0:
        # os.system('cd %s' % os.environ['SNAP_ROOT'])
        cmd = r'%s G:\gdSAR\snap_exps\step5_gpt.xml -Pinput1="%s\step3.dim" -Pinput2="%s\SNAPHU\step3\%s" -Poutput1="%s\step5.dim"' % (SNAP_MAIN_EXE, OUTPUT_DIR, OUTPUT_DIR, filename[0], OUTPUT_DIR)
        print(cmd)
        os.system(cmd)

else:
    OUTPUT_DIR_prefix = OUTPUT_DIR.split('_')[0]
    start_id = int(sys.argv[2])
    end_id = int(sys.argv[3])
    save_filename = OUTPUT_DIR_prefix + r'_%d\Stack.dim'%(end_id+1)
    dirs = []
    for i in range(start_id, end_id+1):
        dirs.append('%s_%d_%d\\step8.dim'%(OUTPUT_DIR_prefix, i, i+1))
    input_filename = ','.join(dirs)
    cmd = r'%s G:\gdSAR\snap_exps\step7_gpt.xml -Pinput1="%s" -Poutput1="%s"'%(SNAP_MAIN_EXE, input_filename, save_filename)
    print(cmd)
    os.system(cmd)
