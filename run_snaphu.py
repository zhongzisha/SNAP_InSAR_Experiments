import os, glob
print(os.environ['SNAP_ROOT'])
SNAP_ROOT = os.environ['SNAP_ROOT']

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
    cmd = r'java -cp "%s\modules\*;%s\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%s" -Xmx12G org.esa.snap.runtime.Launcher G:\gdSAR\snap_exps\step5_gpt.xml -Pinput1="E:\outputs\step3.dim" -Pinput2="E:\outputs\SNAPHU\step3\%s" -Poutput1="E:\outputs\step5.dim"' % (SNAP_ROOT, SNAP_ROOT, SNAP_ROOTfilename[0])
    print(cmd)
    os.system(cmd)

