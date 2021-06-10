set SNAP_ROOT=E:\SNAP\snap-engine-9.0.0-SNAPSHOT
set OUTPUT_DIR=%3
set SNAP_MAIN_EXE=java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Djava.library.path="%SNAP_ROOT%\lib" -Xmx12G org.esa.snap.runtime.Launcher

echo %SNAP_MAIN_EXE%

cd %SNAP_ROOT%

E:

if not exist "%OUTPUT_DIR%\step1.dim" (
%SNAP_MAIN_EXE% ^
G:\gdSAR\snap_exps\step1_gpt.xml ^
-Pinput1="G:\gdSAR\%1" ^
-Pinput2="G:\gdSAR\%2" ^
-Poutput1="%OUTPUT_DIR%\step1.dim"
)


if not exist "%OUTPUT_DIR%\step2.dim" (
%SNAP_MAIN_EXE% ^
G:\gdSAR\snap_exps\step2_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step1.dim" ^
-Poutput1="%OUTPUT_DIR%\step2.dim"
)

if not exist "%OUTPUT_DIR%\step3.dim" (
%SNAP_MAIN_EXE% ^
G:\gdSAR\snap_exps\step3_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step2.dim" ^
-Poutput1="%OUTPUT_DIR%\step3.dim"
)

if not exist "%OUTPUT_DIR%\SNAPHU\snaphu.conf" (
%SNAP_MAIN_EXE% ^
G:\gdSAR\snap_exps\step4_gpt.xml ^
-Pinput1="%OUTPUT_DIR%\step3.dim" ^
-Poutput1="%OUTPUT_DIR%\SNAPHU"
)

cd "%OUTPUT_DIR%\SNAPHU\step3"

python G:\gdSAR\snap_exps\run_snaphu.py

cd %SNAP_ROOT%

if not exist "%OUTPUT_DIR%\step6.dim" (
%SNAP_MAIN_EXE% ^
PhaseToDisplacement ^
-Ssource="%OUTPUT_DIR%\step5.dim" ^
-t "%OUTPUT_DIR%\step6.dim"
)

if not exist "%OUTPUT_DIR%\step7.dim" (
%SNAP_MAIN_EXE% ^
Terrain-Correction ^
-Ssource="%OUTPUT_DIR%\step6.dim" ^
-PsaveDEM=true ^
-t "%OUTPUT_DIR%\step7.dim"
)

if exist "%OUTPUT_DIR%\step7.dim" (
rd /s /q "%OUTPUT_DIR%\step1.data"
rd /s /q "%OUTPUT_DIR%\step2.data"
rd /s /q "%OUTPUT_DIR%\step3.data"
rd /s /q "%OUTPUT_DIR%\SNAPHU"
rd /s /q "%OUTPUT_DIR%\step5.data"
rd /s /q "%OUTPUT_DIR%\step6.data"
del %OUTPUT_DIR%\step1.dim
del %OUTPUT_DIR%\step2.dim
del %OUTPUT_DIR%\step3.dim
del %OUTPUT_DIR%\step5.dim
del %OUTPUT_DIR%\step6.dim
)


