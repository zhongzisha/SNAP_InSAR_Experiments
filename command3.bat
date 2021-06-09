set SNAP_ROOT="E:\SNAP\snap-engine-9.0.0-SNAPSHOT"

cd %SNAP_ROOT%

E:

java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step1_gpt.xml ^
-Pinput1="G:\gdSAR\S1A_IW_SLC__1SDV_20191004T103353_20191004T103421_029308_0354A6_2821.SAFE" ^
-Pinput2="G:\gdSAR\S1A_IW_SLC__1SDV_20191028T103353_20191028T103421_029658_0360B8_7142.SAFE" ^
-Poutput1="E:\outputs\step1.dim"


java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step2_gpt.xml ^
-Pinput1="E:\outputs\step1.dim" ^
-Poutput1="E:\outputs\step2.dim"

java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step3_gpt.xml ^
-Pinput1="E:\outputs\step2.dim" ^
-Poutput1="E:\outputs\step3.dim"

java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step4_gpt.xml ^
-Pinput1="E:\outputs\step3.dim" ^
-Poutput1="E:\outputs\SNAPHU"

cd "E:\outputs\SNAPHU\step3"

python G:\gdSAR\snap_exps\run_snaphu.py

cd %SNAP_ROOT%

java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
PhaseToDisplacement ^
-Ssource="E:\outputs\step5.dim" ^
-t "E:\outputs\step6.dim"

java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
Terrain-Correction ^
-Ssource="E:\outputs\step6.dim" ^
-PsaveDEM=true ^
-t "E:\outputs\step7.dim"




