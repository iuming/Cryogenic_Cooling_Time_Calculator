#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: utils/font_utils.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Font utilities for handling Chinese font display in matplotlib plots.
    Provides automatic detection of available Chinese fonts and safe font
    configuration for cross-platform compatibility.

Key Functions:
    - detect_chinese_fonts(): Detect available Chinese fonts on system
    - setup_chinese_font(): Configure matplotlib for Chinese display
    - get_safe_font(): Get safe font configuration with fallbacks
    - test_font_display(): Test font rendering functionality

Supported Fonts:
    - SimHei (黑体)
    - Microsoft YaHei (微软雅黑)
    - FangSong (仿宋)
    - KaiTi (楷体)
    - STSong, STHeiti (macOS fonts)

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial implementation for font detection
    2025-07-27, Ming Liu: Added safe font configuration with fallbacks
    2025-07-27, Ming Liu: Added font testing functionality
    2025-07-27, Ming Liu: Added comprehensive documentation and headers
==============================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings

def detect_chinese_fonts():
    """
    检测系统中可用的中文字体
    
    Returns:
        list: 可用的中文字体列表
    """
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'FangSong', 'KaiTi', 'STSong', 'STHeiti']
    
    found_fonts = []
    for font in chinese_fonts:
        if font in available_fonts:
            found_fonts.append(font)
    
    return found_fonts

def setup_chinese_font():
    """
    设置matplotlib中文字体
    
    Returns:
        bool: 设置是否成功
    """
    found_fonts = detect_chinese_fonts()
    
    if found_fonts:
        plt.rcParams['font.sans-serif'] = found_fonts
        plt.rcParams['axes.unicode_minus'] = False
        return True
    else:
        warnings.warn("未找到中文字体，将使用默认字体", UserWarning)
        return False

def get_safe_font():
    """
    获取安全的字体设置（支持中英文）
    
    Returns:
        dict: matplotlib字体参数
    """
    found_fonts = detect_chinese_fonts()
    
    if found_fonts:
        return {
            'font.sans-serif': found_fonts + ['DejaVu Sans', 'Arial'],
            'axes.unicode_minus': False
        }
    else:
        return {
            'font.sans-serif': ['DejaVu Sans', 'Arial'],
            'axes.unicode_minus': False
        }

def test_font_display():
    """测试字体显示效果"""
    import numpy as np
    
    setup_chinese_font()
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    ax.plot(x, y, label='测试曲线')
    ax.set_xlabel('时间 (s)')
    ax.set_ylabel('温度 (K)')
    ax.set_title('中文字体测试图表')
    ax.legend()
    ax.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return True

if __name__ == "__main__":
    print("检测中文字体...")
    fonts = detect_chinese_fonts()
    if fonts:
        print(f"找到字体: {', '.join(fonts)}")
        test_font_display()
    else:
        print("未找到中文字体")
