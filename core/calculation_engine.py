#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: core/calculation_engine.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Core calculation engine for cryogenic cooling time analysis. Implements
    physics-based models for heat capacity, heat leak analysis, and multi-stage
    cooling calculations. Uses Debye model for low-temperature heat capacity
    and comprehensive heat transfer modeling.

Key Classes:
    - CryogenicCalculationEngine: Main calculation engine
    
Key Functions:
    - debye_heat_capacity(): Temperature-dependent heat capacity calculation
    - calculate_heat_leak(): Heat leak analysis with multiple contributions
    - calculate_cooling_stages(): Multi-stage cooling time computation
    - get_temperature_profile(): Temperature-time curve generation

Physics Models:
    - Debye model for heat capacity at low temperatures
    - Stefan-Boltzmann radiation heat transfer
    - Residual gas conduction analysis
    - Multi-layer insulation (MLI) effectiveness

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial implementation with Debye model
    2025-07-27, Ming Liu: Added heat leak analysis
    2025-07-27, Ming Liu: Fixed array condition handling in integrand function
    2025-07-27, Ming Liu: Added comprehensive documentation and headers
==============================================================================
"""

import numpy as np

class CryogenicCalculationEngine:
    """低温冷却计算引擎"""
    
    def __init__(self):
        """初始化计算引擎"""
        # 材料密度 (kg/m³)
        self.density_nb = 8570  # 铌
        self.density_cu = 8960  # 铜
        
        # 德拜温度 (K)
        self.theta_D_nb = 275   # 铌
        self.theta_D_cu = 343   # 铜
    
    def debye_heat_capacity(self, T, theta_D):
        """
        德拜模型计算比热容
        
        Args:
            T (float): 温度 (K)
            theta_D (float): 德拜温度 (K)
        
        Returns:
            float: 比热容 (J/kg/K)
        """
        if T <= 0:
            return 0
        
        x = theta_D / T
        if x > 50:  # 极低温近似
            return 12 * np.pi**4 * 8.314 * (T/theta_D)**3 / 5
        
        # 数值积分德拜函数
        def integrand(t):
            return np.where(t > 50, 0, t**4 * np.exp(t) / (np.exp(t) - 1)**2)
        
        # 简化的数值积分
        t_vals = np.linspace(0.01, x, 1000)
        integrand_vals = integrand(t_vals)
        integral = np.trapz(integrand_vals, t_vals)
        
        return 9 * 8.314 * (T/theta_D)**3 * integral
    
    def calculate_heat_leak(self, T_cold, T_warm=300, vacuum_level=1e-3):
        """
        计算热泄漏
        
        Args:
            T_cold (float): 冷端温度 (K)
            T_warm (float): 热端温度 (K)
            vacuum_level (float): 真空度 (Pa)
        
        Returns:
            dict: 各种热泄漏贡献
        """
        # 辐射热泄漏 (Stefan-Boltzmann定律)
        sigma = 5.67e-8  # W/m²/K⁴
        emissivity = 0.05  # 多层隔热的有效发射率
        area = 5.0  # m² (估算有效面积)
        
        Q_radiation = emissivity * sigma * area * (T_warm**4 - T_cold**4)
        
        # 残余气体导热
        if vacuum_level > 1e-4:
            # 分子流区域
            pressure_factor = vacuum_level / 1e-3
            Q_gas = 0.02 * pressure_factor * (T_warm - T_cold) / T_cold
        else:
            Q_gas = 0.001  # 极好真空下的残余导热
        
        # 支撑结构导热
        Q_support = 0.05 * (T_warm - T_cold) / (T_warm + T_cold)
        
        # 总热泄漏
        Q_total = Q_radiation + Q_gas + Q_support
        
        return {
            'radiation': Q_radiation,
            'gas_conduction': Q_gas,
            'support_conduction': Q_support,
            'total': Q_total
        }
    
    def calculate_cooling_stages(self, T_start=300, T_end=4.2, num_stages=20,
                               cooling_power=1.0, copper_mass=1.613, sample_mass=0.024):
        """
        分阶段计算冷却时间
        
        Args:
            T_start (float): 起始温度 (K)
            T_end (float): 终止温度 (K)
            num_stages (int): 分段数量
            cooling_power (float): 制冷功率 (W)
            copper_mass (float): 铜质量 (kg)
            sample_mass (float): 样品质量 (kg)
        
        Returns:
            dict: 分段计算结果
        """
        # 对数分段（低温段密度更高）
        T_log_start = np.log(T_start)
        T_log_end = np.log(T_end)
        T_log_points = np.linspace(T_log_start, T_log_end, num_stages + 1)
        T_points = np.exp(T_log_points)
        
        stages = []
        total_time = 0
        
        for i in range(num_stages):
            T_high = T_points[i]
            T_low = T_points[i + 1]
            T_avg = (T_high + T_low) / 2
            
            # 平均比热容
            C_cu_avg = self.debye_heat_capacity(T_avg, self.theta_D_cu)
            C_nb_avg = self.debye_heat_capacity(T_avg, self.theta_D_nb)
            
            # 总热容量
            C_total = copper_mass * C_cu_avg + sample_mass * C_nb_avg  # J/K
            
            # 需要移除的热量
            Q_remove = C_total * (T_high - T_low)  # J
            
            # 热泄漏
            heat_leak_info = self.calculate_heat_leak(T_avg)
            heat_leak = heat_leak_info['total']
            
            # 净制冷功率
            net_power = cooling_power - heat_leak
            
            if net_power > 0:
                stage_time = Q_remove / net_power  # 秒
                total_time += stage_time
                
                stage_result = {
                    'stage': i + 1,
                    'T_start': T_high,
                    'T_end': T_low,
                    'T_avg': T_avg,
                    'heat_capacity_total': C_total,
                    'heat_removal': Q_remove,
                    'heat_leak': heat_leak,
                    'net_power': net_power,
                    'time_seconds': stage_time,
                    'time_hours': stage_time / 3600,
                    'success': True
                }
            else:
                stage_result = {
                    'stage': i + 1,
                    'T_start': T_high,
                    'T_end': T_low,
                    'T_avg': T_avg,
                    'heat_capacity_total': C_total,
                    'heat_removal': Q_remove,
                    'heat_leak': heat_leak,
                    'net_power': net_power,
                    'time_seconds': 0,
                    'time_hours': 0,
                    'success': False
                }
            
            stages.append(stage_result)
            
            if not stage_result['success']:
                break
        
        return {
            'stages': stages,
            'total_time_seconds': total_time,
            'total_time_hours': total_time / 3600,
            'total_time_days': total_time / (3600 * 24),
            'successful_stages': len([s for s in stages if s['success']]),
            'final_temperature': stages[-1]['T_end'] if stages else T_start
        }
    
    def get_temperature_profile(self, calculation_results):
        """
        获取温度-时间曲线数据
        
        Args:
            calculation_results (dict): 计算结果
        
        Returns:
            tuple: (时间数组, 温度数组)
        """
        times = [0]
        temperatures = []
        
        cumulative_time = 0
        
        for stage in calculation_results['stages']:
            if stage['success']:
                temperatures.append(stage['T_start'])
                cumulative_time += stage['time_hours']
                times.append(cumulative_time)
                temperatures.append(stage['T_end'])
            else:
                temperatures.append(stage['T_start'])
                break
        
        return np.array(times), np.array(temperatures)

# 便捷函数
def calculate_cooling_time(cooling_power=1.0, copper_mass=1.613, sample_mass=0.024):
    """
    便捷的冷却时间计算函数
    
    Returns:
        dict: 计算结果
    """
    engine = CryogenicCalculationEngine()
    return engine.calculate_cooling_stages(
        cooling_power=cooling_power,
        copper_mass=copper_mass,
        sample_mass=sample_mass
    )
