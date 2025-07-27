#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: utils/test_utils.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Testing utilities for validating system components and functionality.
    Provides comprehensive testing suite for imports, calculation engine,
    font utilities, GUI components, and overall system integration.

Test Categories:
    - Module imports and dependencies
    - Core calculation engine functionality
    - Font handling and display capabilities
    - GUI component creation and functionality
    - System integration and performance

Key Functions:
    - test_imports(): Validate required module imports
    - test_calculation_engine(): Test physics calculations
    - test_font_utils(): Verify font handling
    - test_gui_components(): Check GUI functionality
    - run_all_tests(): Comprehensive system validation

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial testing framework implementation
    2025-07-27, Ming Liu: Added comprehensive component testing
    2025-07-27, Ming Liu: Added GUI testing without display
    2025-07-27, Ming Liu: Added comprehensive documentation and headers
==============================================================================
"""

import sys
import traceback

def test_imports():
    """测试必要模块的导入"""
    print("测试模块导入...")
    
    try:
        import numpy as np
        print("✓ numpy 导入成功")
    except ImportError as e:
        print(f"✗ numpy 导入失败: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib 导入成功")
    except ImportError as e:
        print(f"✗ matplotlib 导入失败: {e}")
        return False
    
    try:
        import tkinter as tk
        print("✓ tkinter 导入成功")
    except ImportError as e:
        print(f"✗ tkinter 导入失败: {e}")
        return False
    
    return True

def test_calculation_engine():
    """测试计算引擎"""
    print("\n测试计算引擎...")
    
    try:
        from core.calculation_engine import CryogenicCalculationEngine
        
        engine = CryogenicCalculationEngine()
        
        # 测试德拜比热容计算
        C_test = engine.debye_heat_capacity(100, 275)
        if C_test > 0:
            print(f"✓ 德拜比热容计算正常: {C_test:.2f} J/kg/K")
        else:
            print("✗ 德拜比热容计算异常")
            return False
        
        # 测试热泄漏计算
        heat_leak = engine.calculate_heat_leak(50)
        if heat_leak['total'] > 0:
            print(f"✓ 热泄漏计算正常: {heat_leak['total']:.3f} W")
        else:
            print("✗ 热泄漏计算异常")
            return False
        
        print("✓ 计算引擎测试通过")
        return True
        
    except Exception as e:
        print(f"✗ 计算引擎测试失败: {e}")
        traceback.print_exc()
        return False

def test_font_utils():
    """测试字体工具"""
    print("\n测试字体工具...")
    
    try:
        from utils.font_utils import detect_chinese_fonts, setup_chinese_font
        
        fonts = detect_chinese_fonts()
        print(f"✓ 检测到 {len(fonts)} 个中文字体")
        
        success = setup_chinese_font()
        if success:
            print("✓ 中文字体设置成功")
        else:
            print("⚠ 中文字体设置失败，将使用默认字体")
        
        return True
        
    except Exception as e:
        print(f"✗ 字体工具测试失败: {e}")
        traceback.print_exc()
        return False

def test_simple_calculator():
    """测试简单计算器"""
    print("\n测试简单计算器...")
    
    try:
        from scripts.simple_calculator import calculate_simple_cooling_time
        
        results = calculate_simple_cooling_time()
        
        if results['total_time_hours'] > 0:
            print(f"✓ 简单计算器工作正常: {results['total_time_hours']:.1f} 小时")
            return True
        else:
            print("✗ 简单计算器结果异常")
            return False
        
    except Exception as e:
        print(f"✗ 简单计算器测试失败: {e}")
        traceback.print_exc()
        return False

def test_gui_components():
    """测试GUI组件（无显示）"""
    print("\n测试GUI组件...")
    
    try:
        import tkinter as tk
        
        # 创建隐藏的测试窗口
        root = tk.Tk()
        root.withdraw()  # 隐藏窗口
        
        # 测试基本组件
        frame = tk.Frame(root)
        label = tk.Label(frame, text="测试标签")
        button = tk.Button(frame, text="测试按钮")
        
        print("✓ tkinter 组件创建成功")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ GUI组件测试失败: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("组件测试开始")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_calculation_engine,
        test_font_utils,
        test_simple_calculator,
        test_gui_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"测试异常: {e}")
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed}/{total} 通过")
    print("=" * 50)
    
    if passed == total:
        print("🎉 所有测试通过！系统可以正常运行。")
        return True
    else:
        print("⚠️  部分测试失败，请检查依赖和配置。")
        return False

if __name__ == "__main__":
    run_all_tests()
