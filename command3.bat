set SNAP_ROOT=E:\SNAP\snap-engine-9.0.0-SNAPSHOT
set SNAP_MAIN_EXE=java -cp "%SNAP_ROOT%\modules\*;%SNAP_ROOT%\lib\*" -Dsnap.mainClass=org.esa.snap.core.gpf.main.GPT -Dsnap.home="%SNAP_ROOT%" -Djava.library.path="%SNAP_ROOT%\lib" -Xmx12G org.esa.snap.runtime.Launcher

echo %SNAP_MAIN_EXE%

cd %SNAP_ROOT%

E:

REM set OUTPUT_DIR=%3

REM if not exist "%OUTPUT_DIR%\step1.dim" (
REM %SNAP_MAIN_EXE% ^
REM G:\gdSAR\snap_exps\step1_gpt.xml ^
REM -Pinput1="G:\gdSAR\%1" ^
REM -Pinput2="G:\gdSAR\%2" ^
REM -Poutput1="%OUTPUT_DIR%\step1.dim"
REM )


REM if not exist "%OUTPUT_DIR%\step2.dim" (
REM %SNAP_MAIN_EXE% ^
REM G:\gdSAR\snap_exps\step2_gpt.xml ^
REM -Pinput1="%OUTPUT_DIR%\step1.dim" ^
REM -Poutput1="%OUTPUT_DIR%\step2.dim"
REM )

REM if not exist "%OUTPUT_DIR%\step3.dim" (
REM %SNAP_MAIN_EXE% ^
REM G:\gdSAR\snap_exps\step3_gpt.xml ^
REM -Pinput1="%OUTPUT_DIR%\step2.dim" ^
REM -Poutput1="%OUTPUT_DIR%\step3.dim"
REM )

REM if not exist "%OUTPUT_DIR%\SNAPHU\snaphu.conf" (
REM %SNAP_MAIN_EXE% ^
REM G:\gdSAR\snap_exps\step4_gpt.xml ^
REM -Pinput1="%OUTPUT_DIR%\step3.dim" ^
REM -Poutput1="%OUTPUT_DIR%\SNAPHU"
REM )

REM cd "%OUTPUT_DIR%\SNAPHU\step3"

REM python G:\gdSAR\snap_exps\run_snaphu.py 0

REM cd %SNAP_ROOT%

REM if not exist "%OUTPUT_DIR%\step6.dim" (
REM %SNAP_MAIN_EXE% ^
REM PhaseToDisplacement ^
REM -Ssource="%OUTPUT_DIR%\step5.dim" ^
REM -t "%OUTPUT_DIR%\step6.dim"
REM )

REM REM stacking
REM if not exist "%OUTPUT_DIR%\step7.dim" (
REM %SNAP_MAIN_EXE% ^
REM G:\gdSAR\snap_exps\step6_gpt.xml ^
REM -Pinput1="%OUTPUT_DIR%\step6.dim,%OUTPUT_DIR%\step5.dim" ^
REM -Poutput1="%OUTPUT_DIR%\step7.dim"
REM )

REM if not exist "%OUTPUT_DIR%\step8.dim" (
REM %SNAP_MAIN_EXE% ^
REM Terrain-Correction ^
REM -Ssource="%OUTPUT_DIR%\step7.dim" ^
REM -PsaveDEM=true ^
REM -t "%OUTPUT_DIR%\step8.dim"
REM )

REM if exist "%OUTPUT_DIR%\step7.dim" (
REM rd /s /q "%OUTPUT_DIR%\step1.data"
REM rd /s /q "%OUTPUT_DIR%\step2.data"
REM rd /s /q "%OUTPUT_DIR%\step3.data"
REM rd /s /q "%OUTPUT_DIR%\SNAPHU"
REM rd /s /q "%OUTPUT_DIR%\step5.data"
REM rd /s /q "%OUTPUT_DIR%\step6.data"
REM rd /s /q "%OUTPUT_DIR%\step7.data"
REM del %OUTPUT_DIR%\step1.dim
REM del %OUTPUT_DIR%\step2.dim
REM del %OUTPUT_DIR%\step3.dim
REM del %OUTPUT_DIR%\step5.dim
REM del %OUTPUT_DIR%\step6.dim
REM del %OUTPUT_DIR%\step7.dim
REM )

set OUTPUT_DIR=%1
python G:\gdSAR\snap_exps\run_snaphu.py 1 8 14


