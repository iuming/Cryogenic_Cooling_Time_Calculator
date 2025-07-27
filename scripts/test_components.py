#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: scripts/test_components.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Component testing script for independent module functionality validation.
    Tests core calculation engines, visualization components, and system
    integration without requiring GUI display. Suitable for CI/CD pipelines
    and automated testing environments.

Test Coverage:
    - Core calculation engine functionality
    - Simplified calculation algorithms
    - Matplotlib plotting without display
    - Module import and dependency validation
    - Cross-platform compatibility

Key Functions:
    - test_calculation_only(): Core engine testing
    - test_simple_calculation(): Simplified algorithms
    - test_matplotlib_basic(): Plotting functionality
    - main(): Test orchestration and reporting

Usage:
    python scripts/test_components.py

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial component testing framework
    2025-07-27, Ming Liu: Added matplotlib headless testing
    2025-07-27, Ming Liu: Added comprehensive error handling
    2025-07-27, Ming Liu: Added comprehensive documentation and headers
==============================================================================
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_calculation_only():
    """仅测试计算功能，不涉及GUI"""
    print("测试核心计算功能...")
    
    try:
        from core.calculation_engine import CryogenicCalculationEngine
        
        # 创建计算引擎
        engine = CryogenicCalculationEngine()
        
        # 测试德拜热容计算
        heat_capacity = engine.debye_heat_capacity(100, 275)
        print(f"✓ 德拜热容计算: C(100K) = {heat_capacity:.2f} J/kg/K")
        
        # 测试热泄漏计算
        heat_leak = engine.calculate_heat_leak(100, 300, 1e-3)
        print(f"✓ 热泄漏计算: {heat_leak['total']:.4f} W")
        
        print(f"✓ 核心计算引擎测试通过")
        
        return True
        
    except Exception as e:
        print(f"✗ 计算测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_calculation():
    """测试简化计算"""
    print("\n测试简化计算...")
    
    try:
        from scripts.simple_calculator import calculate_simple_cooling_time
        
        results = calculate_simple_cooling_time()
        
        print(f"✓ 简化计算完成")
        print(f"  理论时间: {results['total_time_hours']:.1f} 小时")
        print(f"  工程时间: {results['engineering_time_hours']:.1f} 小时")
        
        return True
        
    except Exception as e:
        print(f"✗ 简化计算测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_matplotlib_basic():
    """测试matplotlib基本功能"""
    print("\n测试matplotlib...")
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # 使用非交互式后端
        import matplotlib.pyplot as plt
        import numpy as np
        
        # 创建简单图表
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Test Plot')
        
        print("✓ matplotlib 基本功能正常")
        plt.close(fig)
        return True
        
    except Exception as e:
        print(f"✗ matplotlib 测试失败: {e}")
        return False

if __name__ == "__main__":
    print("=" * 40)
    print("组件独立测试")
    print("=" * 40)
    
    tests = [
        test_calculation_only,
        test_simple_calculation, 
        test_matplotlib_basic
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n测试结果: {passed}/{len(tests)} 通过")
    
    if passed == len(tests):
        print("🎉 核心功能测试通过！")
    else:
        print("⚠️  部分功能存在问题")
