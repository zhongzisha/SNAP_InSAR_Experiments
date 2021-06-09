import os, glob
print(os.environ['SNAP_ROOT'])
SNAP_ROOT = os.environ['SNAP_ROOT']
OUTPUT_DIR = os.environ['OUTPUT_DIR']

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
        os.system(cmd)

filename = glob.glob('UnwPhase_ifg_*.snaphu.hdr')
if len(filename) > 0:
    # os.system('cd %s' % os.environ['SNAP_ROOT'])
    cmd = r'java -cp "%s\modules\*;%s\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%s" -Xmx12G org.esa.snap.runtime.Launcher G:\gdSAR\snap_exps\step5_gpt.xml -Pinput1="%s\step3.dim" -Pinput2="%s\SNAPHU\step3\%s" -Poutput1="%s\step5.dim"' % (SNAP_ROOT, SNAP_ROOT, SNAP_ROOT, OUTPUT_DIR,  OUTPUT_DIR, filename[0], OUTPUT_DIR)
    print(cmd)
    os.system(cmd)

