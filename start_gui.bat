@echo off
chcp 65001 > nul
echo ==========================================
echo    Cryogenic Cooling Time Calculator v1.0.0
echo    低温冷却时间计算器
echo.
echo    Author: Ming Liu (刘铭)
echo    Institution: Key Laboratory of Particle 
echo                 Acceleration Physics and Technology
echo                 Chinese Academy of Sciences
echo ==========================================
echo.
echo Starting GUI application...
echo 正在启动GUI应用程序...
echo.

python cooling_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ==========================================
    echo ERROR: Failed to start the application
    echo 错误：应用程序启动失败
    echo ==========================================
    echo.
    echo Please check the following:
    echo 请检查以下项目：
    echo.
    echo 1. Python is installed and accessible
    echo    Python已安装且可访问
    echo.
    echo 2. Required packages are installed:
    echo    必要的包已安装：
    echo    - pip install numpy matplotlib
    echo.
    echo 3. Run test script to diagnose:
    echo    运行测试脚本进行诊断：
    echo    - python scripts\test_components.py
    echo.
    pause
) else (
    echo.
    echo Application closed successfully.
    echo 应用程序已成功关闭。
)
