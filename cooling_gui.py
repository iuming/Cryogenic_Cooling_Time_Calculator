#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
==============================================================================
Project: Cryogenic Cooling Time Calculator
File: cooling_gui.py
Author: Ming Liu (刘铭)
Email: ming-1018@foxmail.com
Institution: Key Laboratory of Particle Acceleration Physics and Technology, 
             Chinese Academy of Sciences
GitHub: @iuming
==============================================================================

Description:
    Main GUI application for calculating cooling time of niobium samples in 
    cryocooler systems. Provides interactive interface with parameter input,
    results display, visualization charts, and system schematic diagrams.
    Supports both Chinese and English interfaces.

Features:
    - Interactive parameter setting with real-time validation
    - Multi-threaded calculation with progress indication
    - Comprehensive results display and analysis
    - Cooling curves and heat capacity visualization
    - Interactive cryostat structure schematic
    - Dual-language support (Chinese/English)

Dependencies:
    - tkinter: GUI framework
    - matplotlib: Plotting and visualization
    - numpy: Numerical calculations
    - threading: Multi-threaded operations

Created: 2025-07-27
Last Modified: 2025-07-27

Change Log:
    2025-07-27, Ming Liu: Initial version with complete GUI functionality
    2025-07-27, Ming Liu: Added system schematic diagrams
    2025-07-27, Ming Liu: Fixed Chinese font display issues
    2025-07-27, Ming Liu: Added proper code headers and documentation
==============================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

# 设置中文字体
def setup_chinese_font():
    """设置matplotlib的中文字体"""
    import matplotlib.font_manager as fm
    
    # 尝试不同的中文字体
    chinese_fonts = ['SimHei', 'Microsoft YaHei', 'FangSong', 'KaiTi', 'STSong', 'STHeiti', 'DejaVu Sans']
    
    available_fonts = [f.name for f in fm.fontManager.ttflist]
    
    for font in chinese_fonts:
        if font in available_fonts:
            plt.rcParams['font.sans-serif'] = [font]
            break
    else:
        print("警告：未找到合适的中文字体，图表中的中文可能显示为方框")
        plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 调用字体设置
setup_chinese_font()

class CryogenicCoolingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("低温制冷时间计算器")
        self.root.geometry("1200x800")
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 语言设置
        self.use_chinese = True
        self.setup_language()
        
        # 创建主框架
        self.create_widgets()
        
        # 默认参数
        self.set_default_values()
    
    def setup_language(self):
        """设置语言标签"""
        if self.use_chinese:
            self.labels = {
                'title': '冷却过程分析图表',
                'cooling_curve': '冷却曲线',
                'cooling_curve_log': '冷却曲线（对数坐标）',
                'heat_capacity': '材料比热容随温度变化',
                'heat_leak': '热泄漏随温度变化',
                'time_hours': '时间 (小时)',
                'temperature_k': '温度 (K)',
                'heat_capacity_unit': '比热容 (J/kg·K)',
                'heat_leak_unit': '热泄漏 (W)',
                'target_temp': '目标温度',
                'estimated_time': '预计时间',
                'copper': '铜',
                'niobium': '铌',
                'heat_leak_label': '热泄漏',
                'cooling_power': '制冷功率'
            }
        else:
            self.labels = {
                'title': 'Cooling Process Analysis',
                'cooling_curve': 'Cooling Curve',
                'cooling_curve_log': 'Cooling Curve (Log Scale)',
                'heat_capacity': 'Heat Capacity vs Temperature',
                'heat_leak': 'Heat Leak vs Temperature',
                'time_hours': 'Time (hours)',
                'temperature_k': 'Temperature (K)',
                'heat_capacity_unit': 'Heat Capacity (J/kg·K)',
                'heat_leak_unit': 'Heat Leak (W)',
                'target_temp': 'Target Temperature',
                'estimated_time': 'Estimated Time',
                'copper': 'Copper',
                'niobium': 'Niobium',
                'heat_leak_label': 'Heat Leak',
                'cooling_power': 'Cooling Power'
            }
        
    def create_widgets(self):
        """创建所有控件"""
        # 创建笔记本控件（标签页）
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 参数输入标签页
        self.input_frame = ttk.Frame(notebook)
        notebook.add(self.input_frame, text="参数设置")
        
        # 结果显示标签页
        self.result_frame = ttk.Frame(notebook)
        notebook.add(self.result_frame, text="计算结果")
        
        # 图表显示标签页
        self.plot_frame = ttk.Frame(notebook)
        notebook.add(self.plot_frame, text="结果图表")
        
        # 创建输入界面
        self.create_input_widgets()
        
        # 创建结果界面
        self.create_result_widgets()
        
        # 创建图表界面
        self.create_plot_widgets()
        
    def create_input_widgets(self):
        """创建参数输入界面"""
        # 主框架 - 使用水平分布
        main_frame = ttk.Frame(self.input_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 左侧参数框架
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # 右侧示意图框架
        right_frame = ttk.LabelFrame(main_frame, text="恒温器结构示意图", padding=10)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        # 配置列权重
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # 创建示意图
        self.create_schematic_diagram(right_frame)
        
        # 系统参数组
        system_group = ttk.LabelFrame(left_frame, text="系统参数", padding=10)
        system_group.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(system_group, text="制冷机功率 (W):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.cooling_power_var = tk.StringVar(value="1.0")
        ttk.Entry(system_group, textvariable=self.cooling_power_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(system_group, text="真空度 (Pa):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.vacuum_var = tk.StringVar(value="1e-3")
        ttk.Entry(system_group, textvariable=self.vacuum_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(system_group, text="初始温度 (K):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.T_initial_var = tk.StringVar(value="300")
        ttk.Entry(system_group, textvariable=self.T_initial_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(system_group, text="目标温度 (K):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.T_target_var = tk.StringVar(value="4.2")
        ttk.Entry(system_group, textvariable=self.T_target_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # 样品参数组
        sample_group = ttk.LabelFrame(left_frame, text="铌样品参数", padding=10)
        sample_group.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(sample_group, text="样品数量:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.sample_count_var = tk.StringVar(value="7")
        ttk.Entry(sample_group, textvariable=self.sample_count_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(sample_group, text="长度 (cm):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.sample_length_var = tk.StringVar(value="10")
        ttk.Entry(sample_group, textvariable=self.sample_length_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(sample_group, text="宽度 (mm):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.sample_width_var = tk.StringVar(value="2")
        ttk.Entry(sample_group, textvariable=self.sample_width_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(sample_group, text="高度 (mm):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.sample_height_var = tk.StringVar(value="2")
        ttk.Entry(sample_group, textvariable=self.sample_height_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # 铜板参数组
        copper_group = ttk.LabelFrame(left_frame, text="铜板参数", padding=10)
        copper_group.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(copper_group, text="长度 (cm):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.copper_length_var = tk.StringVar(value="30")
        ttk.Entry(copper_group, textvariable=self.copper_length_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(copper_group, text="宽度 (cm):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.copper_width_var = tk.StringVar(value="20")
        ttk.Entry(copper_group, textvariable=self.copper_width_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(copper_group, text="厚度 (mm):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.copper_thickness_var = tk.StringVar(value="3")
        ttk.Entry(copper_group, textvariable=self.copper_thickness_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 冷屏参数组
        shield_group = ttk.LabelFrame(left_frame, text="冷屏参数", padding=10)
        shield_group.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(shield_group, text="直径 (m):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.shield_diameter_var = tk.StringVar(value="1.2")
        ttk.Entry(shield_group, textvariable=self.shield_diameter_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(shield_group, text="高度 (m):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.shield_height_var = tk.StringVar(value="1.3")
        ttk.Entry(shield_group, textvariable=self.shield_height_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(shield_group, text="厚度 (mm):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.shield_thickness_var = tk.StringVar(value="5")
        ttk.Entry(shield_group, textvariable=self.shield_thickness_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # 多层隔热参数组
        mli_group = ttk.LabelFrame(left_frame, text="多层隔热参数", padding=10)
        mli_group.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        ttk.Label(mli_group, text="外层层数:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.mli_outer_var = tk.StringVar(value="50")
        ttk.Entry(mli_group, textvariable=self.mli_outer_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(mli_group, text="内层层数:").grid(row=0, column=2, sticky=tk.W, pady=2, padx=20)
        self.mli_inner_var = tk.StringVar(value="10")
        ttk.Entry(mli_group, textvariable=self.mli_inner_var, width=10).grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # 计算选项组
        options_group = ttk.LabelFrame(left_frame, text="计算选项", padding=10)
        options_group.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.include_shield_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_group, text="包含冷屏冷却（否则假设冷屏预冷）", 
                       variable=self.include_shield_var).grid(row=0, column=0, sticky=tk.W)
        
        self.use_ln2_precool_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_group, text="使用液氮预冷到77K", 
                       variable=self.use_ln2_precool_var).grid(row=1, column=0, sticky=tk.W)
        
        # 计算按钮
        button_frame = ttk.Frame(left_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        self.calculate_btn = ttk.Button(button_frame, text="开始计算", command=self.start_calculation)
        self.calculate_btn.pack(side=tk.LEFT, padx=10)
        
        self.reset_btn = ttk.Button(button_frame, text="重置参数", command=self.set_default_values)
        self.reset_btn.pack(side=tk.LEFT, padx=10)
        
        self.lang_btn = ttk.Button(button_frame, text="English", command=self.toggle_language)
        self.lang_btn.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(left_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
    def create_result_widgets(self):
        """创建结果显示界面"""
        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(self.result_frame, height=35, width=100)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 添加字体设置
        self.result_text.configure(font=('Consolas', 10))
        
    def create_plot_widgets(self):
        """创建图表显示界面"""
        # 创建matplotlib图表
        self.fig, ((self.ax1, self.ax2), (self.ax3, self.ax4)) = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle(self.labels['title'], fontsize=14, fontweight='bold')
        
        # 将图表嵌入tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 初始化空图表
        self.ax1.set_title(self.labels['cooling_curve'], fontsize=12)
        self.ax1.set_xlabel(self.labels['time_hours'], fontsize=10)
        self.ax1.set_ylabel(self.labels['temperature_k'], fontsize=10)
        self.ax1.grid(True)
        
        self.ax2.set_title(self.labels['cooling_curve_log'], fontsize=12)
        self.ax2.set_xlabel(self.labels['time_hours'], fontsize=10)
        self.ax2.set_ylabel(self.labels['temperature_k'], fontsize=10)
        self.ax2.set_yscale('log')
        self.ax2.grid(True)
        
        self.ax3.set_title(self.labels['heat_capacity'], fontsize=12)
        self.ax3.set_xlabel(self.labels['temperature_k'], fontsize=10)
        self.ax3.set_ylabel(self.labels['heat_capacity_unit'], fontsize=10)
        self.ax3.grid(True)
        
        self.ax4.set_title(self.labels['heat_leak'], fontsize=12)
        self.ax4.set_xlabel(self.labels['temperature_k'], fontsize=10)
        self.ax4.set_ylabel(self.labels['heat_leak_unit'], fontsize=10)
        self.ax4.grid(True)
        
        plt.tight_layout()
        
    def toggle_language(self):
        """切换语言"""
        self.use_chinese = not self.use_chinese
        self.setup_language()
        
        # 更新按钮文字
        if self.use_chinese:
            self.lang_btn.config(text="English")
        else:
            self.lang_btn.config(text="中文")
        
        # 重新绘制示意图以更新标签
        if hasattr(self, 'schematic_ax'):
            self.draw_cryostat_structure()
        
        # 重新创建图表界面以更新标签
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        self.create_plot_widgets()
        
        # 如果有计算结果，重新绘制图表
        if hasattr(self, 'last_results') and hasattr(self, 'last_params'):
            self.update_plots(self.last_results, self.last_params)
    
    def set_default_values(self):
        """设置默认参数值"""
        self.cooling_power_var.set("1.0")
        self.vacuum_var.set("1e-3")
        self.T_initial_var.set("300")
        self.T_target_var.set("4.2")
        self.sample_count_var.set("7")
        self.sample_length_var.set("10")
        self.sample_width_var.set("2")
        self.sample_height_var.set("2")
        self.copper_length_var.set("30")
        self.copper_width_var.set("20")
        self.copper_thickness_var.set("3")
        self.shield_diameter_var.set("1.2")
        self.shield_height_var.set("1.3")
        self.shield_thickness_var.set("5")
        self.mli_outer_var.set("50")
        self.mli_inner_var.set("10")
        self.include_shield_var.set(False)
        self.use_ln2_precool_var.set(False)
        
    def start_calculation(self):
        """开始计算（在新线程中）"""
        try:
            # 禁用按钮，显示进度条
            self.calculate_btn.config(state='disabled')
            self.progress.start()
            
            # 在新线程中执行计算
            thread = Thread(target=self.perform_calculation)
            thread.daemon = True
            thread.start()
            
        except Exception as e:
            messagebox.showerror("错误", f"启动计算时发生错误：{str(e)}")
            self.calculate_btn.config(state='normal')
            self.progress.stop()
    
    def perform_calculation(self):
        """执行计算"""
        try:
            # 获取参数
            params = self.get_parameters()
            
            # 执行计算
            results = self.calculate_cooling_time(params)
            
            # 在主线程中更新界面
            self.root.after(0, self.update_results, results, params)
            
        except Exception as e:
            self.root.after(0, self.show_error, str(e))
    
    def get_parameters(self):
        """获取用户输入的参数"""
        try:
            params = {
                'cooling_power': float(self.cooling_power_var.get()),
                'vacuum_pressure': float(self.vacuum_var.get()),
                'T_initial': float(self.T_initial_var.get()),
                'T_target': float(self.T_target_var.get()),
                'sample_count': int(self.sample_count_var.get()),
                'sample_length': float(self.sample_length_var.get()) / 100,  # cm to m
                'sample_width': float(self.sample_width_var.get()) / 1000,   # mm to m
                'sample_height': float(self.sample_height_var.get()) / 1000,  # mm to m
                'copper_length': float(self.copper_length_var.get()) / 100,  # cm to m
                'copper_width': float(self.copper_width_var.get()) / 100,    # cm to m
                'copper_thickness': float(self.copper_thickness_var.get()) / 1000,  # mm to m
                'shield_diameter': float(self.shield_diameter_var.get()),
                'shield_height': float(self.shield_height_var.get()),
                'shield_thickness': float(self.shield_thickness_var.get()) / 1000,  # mm to m
                'mli_outer': int(self.mli_outer_var.get()),
                'mli_inner': int(self.mli_inner_var.get()),
                'include_shield': self.include_shield_var.get(),
                'use_ln2_precool': self.use_ln2_precool_var.get()
            }
            return params
        except ValueError as e:
            raise ValueError(f"参数输入错误：{str(e)}")
    
    def calculate_cooling_time(self, params):
        """执行冷却时间计算"""
        # 计算质量
        nb_density = 8570  # kg/m³
        copper_density = 8960  # kg/m³
        
        # 样品质量
        sample_volume = (params['sample_length'] * params['sample_width'] * 
                        params['sample_height'])
        sample_mass = sample_volume * nb_density * params['sample_count']
        
        # 铜板质量
        copper_volume = (params['copper_length'] * params['copper_width'] * 
                        params['copper_thickness'])
        copper_mass = copper_volume * copper_density
        
        # 冷屏质量
        outer_radius = params['shield_diameter'] / 2
        inner_radius = outer_radius - params['shield_thickness']
        cylinder_wall_volume = np.pi * (outer_radius**2 - inner_radius**2) * params['shield_height']
        top_bottom_volume = 2 * np.pi * outer_radius**2 * params['shield_thickness']
        shield_volume = cylinder_wall_volume + top_bottom_volume
        shield_mass = shield_volume * copper_density
        
        # 分段计算
        stages = [
            (300, 250, 385, 265, 0.05),
            (250, 200, 385, 265, 0.08),
            (200, 150, 350, 230, 0.10),
            (150, 100, 300, 180, 0.13),
            (100, 77, 200, 120, 0.15),
            (77, 50, 120, 80, 0.16),
            (50, 30, 60, 40, 0.17),
            (30, 20, 30, 20, 0.18),
            (20, 10, 15, 10, 0.185),
            (10, 4.2, 8, 5, 0.19)
        ]
        
        # 根据选项决定计算哪些质量
        if params['include_shield']:
            total_mass = sample_mass + copper_mass + shield_mass
        else:
            total_mass = sample_mass + copper_mass
            
        # 计算各阶段时间
        stage_results = []
        total_time = 0
        total_energy = 0
        
        for T_start, T_end, C_cu, C_nb, heat_leak in stages:
            # 液氮预冷选项
            if params['use_ln2_precool'] and T_start > 77:
                continue
                
            # 计算热容量
            if params['include_shield']:
                C_total = (copper_mass + shield_mass) * C_cu + sample_mass * C_nb
            else:
                C_total = copper_mass * C_cu + sample_mass * C_nb
                
            delta_T = T_start - T_end
            Q_remove = C_total * delta_T
            total_energy += Q_remove
            
            net_power = params['cooling_power'] - heat_leak
            
            if net_power > 0:
                time_hours = Q_remove / (net_power * 3600)
                total_time += time_hours
                
                stage_results.append({
                    'T_start': T_start,
                    'T_end': T_end,
                    'C_cu': C_cu,
                    'C_nb': C_nb,
                    'C_total': C_total,
                    'Q_remove': Q_remove,
                    'heat_leak': heat_leak,
                    'net_power': net_power,
                    'time_hours': time_hours
                })
        
        # 工程修正
        engineering_time = (total_time * 1.2 * 1.1) + 4
        
        # 生成温度曲线数据（简化）
        time_points = np.linspace(0, engineering_time, 1000)
        temp_points = []
        
        current_time = 0
        current_temp = params['T_initial']
        
        for point_time in time_points:
            # 简化的温度衰减模型
            if point_time <= engineering_time:
                progress = point_time / engineering_time
                temp = params['T_initial'] * (1 - progress) + params['T_target'] * progress
                # 添加非线性效果
                temp = params['T_initial'] * np.exp(-3 * progress) + params['T_target']
            else:
                temp = params['T_target']
            temp_points.append(max(temp, params['T_target']))
        
        return {
            'sample_mass': sample_mass,
            'copper_mass': copper_mass,
            'shield_mass': shield_mass,
            'total_mass': total_mass,
            'stage_results': stage_results,
            'total_time': total_time,
            'engineering_time': engineering_time,
            'total_energy': total_energy,
            'time_points': time_points,
            'temp_points': temp_points
        }
    
    def update_results(self, results, params):
        """更新结果显示"""
        try:
            # 保存结果以便语言切换时使用
            self.last_results = results
            self.last_params = params
            
            # 停止进度条，启用按钮
            self.progress.stop()
            self.calculate_btn.config(state='normal')
            
            # 更新文本结果
            self.display_text_results(results, params)
            
            # 更新图表
            self.update_plots(results, params)
            
        except Exception as e:
            self.show_error(f"更新结果时发生错误：{str(e)}")
    
    def display_text_results(self, results, params):
        """显示文本结果"""
        self.result_text.delete(1.0, tk.END)
        
        output = []
        output.append("=" * 70)
        output.append("低温制冷时间计算结果")
        output.append("=" * 70)
        
        # 系统参数
        output.append(f"制冷机功率: {params['cooling_power']} W")
        output.append(f"铌样品: {params['sample_count']}个，总质量 {results['sample_mass']*1000:.1f}g")
        output.append(f"铜板: {params['copper_length']*100:.0f}cm×{params['copper_width']*100:.0f}cm×{params['copper_thickness']*1000:.0f}mm，质量 {results['copper_mass']:.3f}kg")
        
        if params['include_shield']:
            output.append(f"冷屏: 直径{params['shield_diameter']}m×高{params['shield_height']}m×厚{params['shield_thickness']*1000:.0f}mm，质量 {results['shield_mass']:.1f}kg")
            output.append(f"总质量: {results['total_mass']:.1f}kg")
        else:
            output.append("冷屏: 假设已预冷")
            output.append(f"需冷却质量: {results['total_mass']:.3f}kg")
        
        output.append(f"多层隔热: 外层{params['mli_outer']}层 + 内层{params['mli_inner']}层")
        output.append(f"真空度: {params['vacuum_pressure']:.0e} Pa")
        
        if params['use_ln2_precool']:
            output.append("使用液氮预冷到77K")
        
        output.append("")
        
        # 分段结果
        output.append("分段冷却时间:")
        output.append("温度段(K)  铜比热  铌比热  热容(J/K)  热量(kJ)  热泄漏(W)  净功率(W)  时间(h)")
        output.append("-" * 80)
        
        for stage in results['stage_results']:
            output.append(f"{stage['T_start']:3.0f}-{stage['T_end']:3.0f}    "
                         f"{stage['C_cu']:3.0f}     {stage['C_nb']:3.0f}     "
                         f"{stage['C_total']:6.0f}    {stage['Q_remove']/1000:6.0f}    "
                         f"{stage['heat_leak']:.3f}      {stage['net_power']:.3f}      "
                         f"{stage['time_hours']:6.1f}")
        
        output.append("-" * 80)
        output.append(f"理论总时间: {results['total_time']:.1f} 小时 ({results['total_time']/24:.1f} 天)")
        output.append(f"工程估算: {results['engineering_time']:.1f} 小时 ({results['engineering_time']/24:.1f} 天)")
        output.append(f"总移除热量: {results['total_energy']/1000000:.2f} MJ")
        
        # 安全范围
        min_time = results['engineering_time'] * 0.8
        max_time = results['engineering_time'] * 1.3
        output.append("")
        output.append("预计时间范围:")
        output.append(f"  最佳情况: {min_time:.1f} 小时 ({min_time/24:.1f} 天)")
        output.append(f"  一般情况: {results['engineering_time']:.1f} 小时 ({results['engineering_time']/24:.1f} 天)")
        output.append(f"  保守估计: {max_time:.1f} 小时 ({max_time/24:.1f} 天)")
        
        # 建议
        output.append("")
        output.append("工程建议:")
        output.append("1. 确保良好的热接触（使用铟箔或高导热硅脂）")
        output.append("2. 优质的多层隔热安装")
        output.append("3. 稳定的真空度维持")
        output.append("4. 温度分布监控")
        if not params['include_shield']:
            output.append("5. 建议冷屏预冷以缩短总时间")
        if not params['use_ln2_precool']:
            output.append("6. 考虑液氮预冷可大幅缩短时间")
        
        # 显示结果
        self.result_text.insert(tk.END, "\n".join(output))
    
    def update_plots(self, results, params):
        """更新图表"""
        # 清除之前的图表
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        
        # 冷却曲线
        self.ax1.plot(results['time_points'], results['temp_points'], 'b-', linewidth=2, label=self.labels['cooling_curve'])
        self.ax1.axhline(y=params['T_target'], color='r', linestyle='--', 
                        label=f'{self.labels["target_temp"]} {params["T_target"]}K')
        self.ax1.axvline(x=results['engineering_time'], color='g', linestyle='--', 
                        label=f'{self.labels["estimated_time"]} {results["engineering_time"]:.1f}h')
        self.ax1.set_xlabel(self.labels['time_hours'], fontsize=10)
        self.ax1.set_ylabel(self.labels['temperature_k'], fontsize=10)
        self.ax1.set_title(self.labels['cooling_curve'], fontsize=12)
        self.ax1.grid(True)
        self.ax1.legend(prop={'size': 9})
        
        # 对数坐标冷却曲线
        self.ax2.semilogy(results['time_points'], results['temp_points'], 'b-', linewidth=2)
        self.ax2.axhline(y=params['T_target'], color='r', linestyle='--')
        self.ax2.set_xlabel(self.labels['time_hours'], fontsize=10)
        self.ax2.set_ylabel(self.labels['temperature_k'], fontsize=10)
        self.ax2.set_title(self.labels['cooling_curve_log'], fontsize=12)
        self.ax2.grid(True)
        
        # 比热容曲线
        T_range = np.linspace(params['T_target'], params['T_initial'], 100)
        C_copper = []
        C_niobium = []
        
        for T in T_range:
            if T > 50:
                C_cu = 385.0
                C_nb = 265.0
            else:
                # Debye模型近似
                theta_D_cu = 343
                theta_D_nb = 275
                C_cu = 385.0 * (T / theta_D_cu)**3 * 12 * np.pi**4 / 5
                C_nb = 265.0 * (T / theta_D_nb)**3 * 12 * np.pi**4 / 5
            
            C_copper.append(max(C_cu, 0.01))
            C_niobium.append(max(C_nb, 0.01))
        
        self.ax3.plot(T_range, C_copper, label=self.labels['copper'], linewidth=2)
        self.ax3.plot(T_range, C_niobium, label=self.labels['niobium'], linewidth=2)
        self.ax3.set_xlabel(self.labels['temperature_k'], fontsize=10)
        self.ax3.set_ylabel(self.labels['heat_capacity_unit'], fontsize=10)
        self.ax3.set_title(self.labels['heat_capacity'], fontsize=12)
        self.ax3.grid(True)
        self.ax3.legend(prop={'size': 9})
        
        # 热泄漏曲线
        Q_leak = []
        for T in T_range:
            # 简化的热泄漏模型
            if T > 200:
                leak = 0.05
            elif T > 100:
                leak = 0.10
            elif T > 50:
                leak = 0.15
            else:
                leak = 0.18
            Q_leak.append(leak)
        
        self.ax4.plot(T_range, Q_leak, 'r-', linewidth=2, label=self.labels['heat_leak_label'])
        self.ax4.axhline(y=params['cooling_power'], color='b', linestyle='--', 
                        label=f'{self.labels["cooling_power"]} {params["cooling_power"]}W')
        self.ax4.set_xlabel(self.labels['temperature_k'], fontsize=10)
        self.ax4.set_ylabel(self.labels['heat_leak_unit'], fontsize=10)
        self.ax4.set_title(self.labels['heat_leak'], fontsize=12)
        self.ax4.grid(True)
        self.ax4.legend(prop={'size': 9})
        
        plt.tight_layout()
        self.canvas.draw()
    
    def create_schematic_diagram(self, parent_frame):
        """创建恒温器结构示意图"""
        # 创建matplotlib图表
        self.schematic_fig, self.schematic_ax = plt.subplots(figsize=(6, 8))
        
        # 设置坐标范围
        self.schematic_ax.set_xlim(-8, 8)
        self.schematic_ax.set_ylim(-2, 16)
        self.schematic_ax.set_aspect('equal')
        
        # 将图表嵌入tkinter
        self.schematic_canvas = FigureCanvasTkAgg(self.schematic_fig, parent_frame)
        self.schematic_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 绘制恒温器结构
        self.draw_cryostat_structure()
        
        # 隐藏坐标轴
        self.schematic_ax.set_xticks([])
        self.schematic_ax.set_yticks([])
        self.schematic_ax.spines['top'].set_visible(False)
        self.schematic_ax.spines['right'].set_visible(False)
        self.schematic_ax.spines['bottom'].set_visible(False)
        self.schematic_ax.spines['left'].set_visible(False)
        
    def draw_cryostat_structure(self):
        """绘制恒温器结构"""
        import matplotlib.patches as patches
        from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
        
        # 清除之前的图形
        self.schematic_ax.clear()
        self.schematic_ax.set_xlim(-8, 8)
        self.schematic_ax.set_ylim(-2, 16)
        self.schematic_ax.set_aspect('equal')
        
        # 颜色定义
        vacuum_color = '#E8F4FD'  # 淡蓝色 - 真空腔
        shield_color = '#FFE4B5'  # 浅橙色 - 冷屏
        mli_color = '#F0F0F0'     # 浅灰色 - 多层隔热
        copper_color = '#CD853F'  # 铜色 - 铜板
        sample_color = '#C0C0C0'  # 银色 - 铌样品
        cooler_color = '#4169E1'  # 蓝色 - 制冷机
        
        # 1. 真空腔外壳 (最外层)
        vacuum_chamber = Rectangle((-7.5, 0), 15, 15, 
                                 linewidth=3, edgecolor='black', 
                                 facecolor=vacuum_color, alpha=0.3)
        self.schematic_ax.add_patch(vacuum_chamber)
        
        # 2. 多层隔热 (外层 - 50层)
        mli_outer = Rectangle((-6.5, 1), 13, 13, 
                            linewidth=2, edgecolor='gray', 
                            facecolor=mli_color, alpha=0.6,
                            linestyle='--')
        self.schematic_ax.add_patch(mli_outer)
        
        # 3. 冷屏 (直径1.2m, 高度1.3m)
        shield_width = 6
        shield_height = 10
        cold_shield = Rectangle((-shield_width/2, 2.5), shield_width, shield_height,
                              linewidth=2, edgecolor='orange', 
                              facecolor=shield_color, alpha=0.7)
        self.schematic_ax.add_patch(cold_shield)
        
        # 4. 多层隔热 (内层 - 10层，包围样品)
        mli_inner = Rectangle((-2, 6), 4, 4,
                            linewidth=1.5, edgecolor='gray',
                            facecolor=mli_color, alpha=0.8,
                            linestyle=':')
        self.schematic_ax.add_patch(mli_inner)
        
        # 5. 铜板 (30cm × 20cm × 3mm)
        copper_plate = Rectangle((-1.5, 7), 3, 2,
                               linewidth=2, edgecolor='brown',
                               facecolor=copper_color, alpha=0.8)
        self.schematic_ax.add_patch(copper_plate)
        
        # 6. 铌样品 (7个，10cm × 2mm × 2mm)
        sample_positions = [
            (-1.2, 7.3), (-0.6, 7.3), (0, 7.3), (0.6, 7.3), (1.2, 7.3),
            (-0.6, 8.3), (0.6, 8.3)
        ]
        
        for pos in sample_positions:
            sample = Rectangle((pos[0]-0.15, pos[1]), 0.3, 0.4,
                             linewidth=1, edgecolor='black',
                             facecolor=sample_color, alpha=0.9)
            self.schematic_ax.add_patch(sample)
        
        # 7. 制冷机冷头
        cooler_head = Circle((0, 11.5), 0.8,
                           linewidth=2, edgecolor='blue',
                           facecolor=cooler_color, alpha=0.8)
        self.schematic_ax.add_patch(cooler_head)
        
        # 8. 制冷机管道
        cooler_tube = Rectangle((-0.3, 10), 0.6, 3,
                              linewidth=2, edgecolor='blue',
                              facecolor=cooler_color, alpha=0.6)
        self.schematic_ax.add_patch(cooler_tube)
        
        # 9. 热连接导线
        # 制冷机到铜板的连接
        self.schematic_ax.plot([0, 0], [10, 9], 'b-', linewidth=3, alpha=0.8)
        
        # 支撑结构
        support_positions = [(-6, 1), (6, 1), (-3, 2.5), (3, 2.5)]
        for pos in support_positions:
            support = Rectangle((pos[0]-0.1, pos[1]), 0.2, 1,
                              linewidth=1, edgecolor='black',
                              facecolor='gray', alpha=0.5)
            self.schematic_ax.add_patch(support)
        
        # 添加标注
        if self.use_chinese:
            labels = {
                'title': '1W制冷机恒温器结构示意图',
                'vacuum': '真空腔\n(1×10⁻³ Pa)',
                'mli_outer': 'MLI外层\n(50层)',
                'shield': '冷屏\n(铜，φ1.2m×1.3m)',
                'mli_inner': 'MLI内层\n(10层)',
                'copper': '铜板\n(30×20×3mm)',
                'samples': '铌样品\n(7个)',
                'cooler': '1W制冷机\n冷头',
                'connection': '热连接'
            }
        else:
            labels = {
                'title': '1W Cryocooler System Schematic',
                'vacuum': 'Vacuum Chamber\n(1×10⁻³ Pa)',
                'mli_outer': 'MLI Outer\n(50 layers)',
                'shield': 'Cold Shield\n(Cu, φ1.2m×1.3m)',
                'mli_inner': 'MLI Inner\n(10 layers)',
                'copper': 'Copper Plate\n(30×20×3mm)',
                'samples': 'Nb Samples\n(7 pcs)',
                'cooler': '1W Cryocooler\nCold Head',
                'connection': 'Thermal Link'
            }
        
        # 添加标题
        self.schematic_ax.text(0, 15.5, labels['title'], 
                             ha='center', va='center', fontsize=12, fontweight='bold')
        
        # 添加各部件标注
        self.schematic_ax.text(-8.5, 7.5, labels['vacuum'], ha='center', va='center', 
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=vacuum_color, alpha=0.8))
        
        self.schematic_ax.text(8.5, 10, labels['mli_outer'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=mli_color, alpha=0.8))
        
        self.schematic_ax.text(-8.5, 4, labels['shield'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=shield_color, alpha=0.8))
        
        self.schematic_ax.text(4.5, 8, labels['mli_inner'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=mli_color, alpha=0.8))
        
        self.schematic_ax.text(4.5, 7, labels['copper'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=copper_color, alpha=0.8))
        
        self.schematic_ax.text(-4.5, 8, labels['samples'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=sample_color, alpha=0.8))
        
        self.schematic_ax.text(-4.5, 12, labels['cooler'], ha='center', va='center',
                             fontsize=8, bbox=dict(boxstyle="round,pad=0.3", facecolor=cooler_color, alpha=0.8))
        
        # 添加尺寸标注
        # 真空腔尺寸
        self.schematic_ax.annotate('', xy=(7.5, -0.5), xytext=(-7.5, -0.5),
                                 arrowprops=dict(arrowstyle='<->', color='black', lw=1))
        self.schematic_ax.text(0, -1, '1.5m', ha='center', va='center', fontsize=8)
        
        # 冷屏高度
        self.schematic_ax.annotate('', xy=(7, 2.5), xytext=(7, 12.5),
                                 arrowprops=dict(arrowstyle='<->', color='orange', lw=1))
        self.schematic_ax.text(7.8, 7.5, '1.3m', ha='center', va='center', fontsize=8, rotation=90)
        
        # 隐藏坐标轴
        self.schematic_ax.set_xticks([])
        self.schematic_ax.set_yticks([])
        for spine in self.schematic_ax.spines.values():
            spine.set_visible(False)
        
        # 刷新图表（如果canvas已创建）
        if hasattr(self, 'schematic_canvas'):
            self.schematic_canvas.draw()
    
    def show_error(self, error_message):
        """显示错误信息"""
        self.progress.stop()
        self.calculate_btn.config(state='normal')
        messagebox.showerror("计算错误", error_message)

def main():
    """主函数"""
    root = tk.Tk()
    app = CryogenicCoolingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
