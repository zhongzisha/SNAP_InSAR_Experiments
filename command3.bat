set SNAP_ROOT="E:\SNAP\snap-engine-9.0.0-SNAPSHOT"
set OUTPUT_DIR=%3

cd %SNAP_ROOT%

E:

if not exist "%OUTPUT_DIR%\step1.dim" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step1_gpt.xml ^
-Pinput1="G:\gdSAR\%1" ^
-Pinput2="G:\gdSAR\%2" ^
-Poutput1="%OUTPUT_DIR%\step1.dim"
)


if not exist "%OUTPUT_DIR%\step2.dim" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step2_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step1.dim" ^
-Poutput1="%OUTPUT_DIR%\step2.dim"
)

if not exist "%OUTPUT_DIR%\step3.dim" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step3_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step2.dim" ^
-Poutput1="%OUTPUT_DIR%\step3.dim"
)

if not exist "%OUTPUT_DIR%\SNAPHU\snaphu.conf" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
G:\gdSAR\snap_exps\step4_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step3.dim" ^
-Poutput1="%OUTPUT_DIR%\SNAPHU"
)

cd "%OUTPUT_DIR%\SNAPHU\step3"

python G:\gdSAR\snap_exps\run_snaphu.py

cd %SNAP_ROOT%

if not exist "%OUTPUT_DIR%\step6.dim" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
PhaseToDisplacement ^
-Ssource="%OUTPUT_DIR%\step5.dim" ^
-t "%OUTPUT_DIR%\step6.dim"
)

if not exist "%OUTPUT_DIR%\step7.dim" (
java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Xmx12G org.esa.snap.runtime.Launcher ^
Terrain-Correction ^
-Ssource="%OUTPUT_DIR%\step6.dim" ^
-PsaveDEM=true ^
-t "%OUTPUT_DIR%\step7.dim"
)

if exist "%OUTPUT_DIR%\step7.dim" (
rm /s /q "%OUTPUT_DIR%\step1"
rm /s /q "%OUTPUT_DIR%\step2"
rm /s /q "%OUTPUT_DIR%\step3"
rm /s /q "%OUTPUT_DIR%\SNAPHU"
rm /s /q "%OUTPUT_DIR%\step5"
rm /s /q "%OUTPUT_DIR%\step6"
del %OUTPUT_DIR%\step1.dim
del %OUTPUT_DIR%\step2.dim
del %OUTPUT_DIR%\step3.dim
del %OUTPUT_DIR%\step5.dim
del %OUTPUT_DIR%\step6.dim
)


