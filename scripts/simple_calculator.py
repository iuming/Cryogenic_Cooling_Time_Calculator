#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: scripts/simple_calculator.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Simplified cooling time calculator for quick estimation of niobium sample
    cooling in cryogenic systems. Uses piecewise linear approximation for 
    rapid analysis and preliminary design validation.

Key Features:
    - Segmented temperature range analysis (300K to 4.2K)
    - Average heat capacity approximations
    - Simplified heat leak modeling
    - Engineering safety factors
    - Quick performance estimation

Key Functions:
    - calculate_simple_cooling_time(): Main calculation function
    - print_cooling_analysis(): Results display and interpretation
    - main(): Command-line interface

Calculation Method:
    - Temperature-dependent heat capacity averages
    - Stage-wise heat removal analysis
    - Net cooling power with heat leak subtraction
    - Engineering correction factors

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial simplified calculation implementation
    2025-07-27, Ming Liu: Added engineering factors and safety margins
    2025-07-27, Ming Liu: Improved result analysis and display
    2025-07-27, Ming Liu: Added comprehensive documentation and headers
==============================================================================
"""

import numpy as np

def calculate_simple_cooling_time(cooling_power=1.0, copper_mass=1.613, sample_mass=0.024):
    """
    使用分段线性近似计算冷却时间
    
    Args:
        cooling_power (float): 制冷功率 (W)
        copper_mass (float): 铜板质量 (kg)
        sample_mass (float): 样品总质量 (kg)
    
    Returns:
        dict: 包含各段和总冷却时间的结果
    """
    
    # 分段计算参数 (T_start, T_end, C_cu, C_nb)
    stages = [
        (300, 200, 385, 265),  # 高温段
        (200, 100, 300, 200),  # 中温段
        (100, 50, 150, 100),   # 中低温段
        (50, 20, 50, 30),      # 低温段
        (20, 10, 15, 8),       # 更低温段
        (10, 4.2, 5, 2)        # 极低温段
    ]
    
    results = []
    total_time = 0
    
    for T_start, T_end, C_cu, C_nb in stages:
        # 总比热容
        C_total = copper_mass * C_cu + sample_mass * C_nb  # J/K
        
        # 温度变化
        delta_T = T_start - T_end
        
        # 需要移除的热量
        Q_remove = C_total * delta_T  # J
        
        # 平均热泄漏估算
        T_avg = (T_start + T_end) / 2
        if T_avg > 200:
            heat_leak = 0.05  # W
        elif T_avg > 100:
            heat_leak = 0.10  # W
        elif T_avg > 50:
            heat_leak = 0.15  # W
        else:
            heat_leak = 0.18  # W
        
        # 净制冷功率
        net_power = cooling_power - heat_leak  # W
        
        # 时间计算
        if net_power > 0:
            time_hours = Q_remove / (net_power * 3600)
            total_time += time_hours
            
            stage_result = {
                'temperature_range': f"{T_start}-{T_end}K",
                'heat_removal': Q_remove,
                'net_power': net_power,
                'time_hours': time_hours,
                'success': True
            }
        else:
            stage_result = {
                'temperature_range': f"{T_start}-{T_end}K",
                'heat_removal': Q_remove,
                'net_power': net_power,
                'time_hours': 0,
                'success': False
            }
        
        results.append(stage_result)
        
        if not stage_result['success']:
            break
    
    # 工程安全系数
    engineering_factor = 1.5
    actual_time = total_time * engineering_factor
    
    return {
        'stages': results,
        'total_time_hours': total_time,
        'total_time_days': total_time / 24,
        'engineering_time_hours': actual_time,
        'engineering_time_days': actual_time / 24,
        'engineering_factor': engineering_factor
    }

def print_cooling_analysis(results):
    """打印冷却分析结果"""
    
    print("=" * 60)
    print("简化冷却时间估算结果")
    print("=" * 60)
    
    print("温度段\t\t净功率(W)\t时间(h)\t状态")
    print("-" * 50)
    
    for stage in results['stages']:
        status = "✓" if stage['success'] else "✗"
        print(f"{stage['temperature_range']}\t\t{stage['net_power']:.2f}\t\t{stage['time_hours']:.1f}\t{status}")
    
    print("-" * 50)
    print(f"理论总时间: {results['total_time_hours']:.1f} 小时 ({results['total_time_days']:.1f} 天)")
    print(f"工程估算时间: {results['engineering_time_hours']:.1f} 小时 ({results['engineering_time_days']:.1f} 天)")
    print(f"安全系数: {results['engineering_factor']}")
    
    print("\n关键分析:")
    print("• 高温段(300-100K)是主要时间消耗")
    print("• 铜板热容量是主要贡献者")
    print("• 低温段冷却相对较快")
    print("• 工程因素包括温度分布不均匀、热接触阻抗等")

def main():
    """主函数"""
    
    # 默认参数
    cooling_power = 1.0  # W
    copper_mass = 1.613  # kg (30cm × 20cm × 3mm)
    sample_mass = 0.024  # kg (7个样品)
    
    # 计算冷却时间
    results = calculate_simple_cooling_time(cooling_power, copper_mass, sample_mass)
    
    # 打印结果
    print_cooling_analysis(results)
    
    return results

if __name__ == "__main__":
    main()
