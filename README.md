# Cryogenic Cooling Time Calculator

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://iuming.github.io/Cryogenic_Cooling_Time_Calculator/)
[![GitHub Release](https://img.shields.io/github/v/release/iuming/Cryogenic_Cooling_Time_Calculator)](https://github.com/iuming/Cryogenic_Cooling_Time_Calculator/releases)

## English

### Project Overview

A professional tool for calculating cooling time of niobium samples in cryocooler systems. This project provides an intuitive GUI interface with parameter input, results analysis, and chart visualization.

### Features

- 🔧 **Parameterized Calculations**: Support for multiple system parameter configurations
- 📊 **Visualization Analysis**: Cooling curves, heat capacity and heat leak charts
- 🎨 **Dual Language Support**: Chinese/English interface switching
- 🏗️ **System Schematic**: Cryostat structure visualization
- ⚡ **Multi-threaded Calculations**: Prevent interface freezing
- 📋 **Detailed Reports**: Segmented analysis and engineering recommendations

### Tech Stack

- **Python 3.8+**
- **tkinter**: GUI framework
- **matplotlib**: Chart plotting
- **numpy**: Numerical calculations

### Installation & Usage

#### 1. Requirements

```bash
Python 3.8+
```

#### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 3. Run Application

**Method 1: Direct Python execution**
```bash
python cooling_gui.py
```

**Method 2: Windows batch file**
```bash
start_gui.bat
```

### Physics Models

#### Debye Model
- Low-temperature heat capacity calculations
- Material property analysis

#### Heat Transfer Analysis
- Stefan-Boltzmann radiation heat transfer
- Residual gas conduction
- Multi-layer insulation (MLI) effects

#### Multi-stage Cooling
- Temperature-segmented calculations
- Engineering correction factors
- Safety time estimates

### Contributing

Welcome to submit Issues and Pull Requests to improve the project!

### License

[MIT License](LICENSE)

### Author

**Ming Liu (刘铭)**
- Email: ming-1018@foxmail.com
- Institution: Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences
- GitHub: [@iuming](https://github.com/iuming)

---

## 中文

### 项目简介

低温制冷时间计算器是一个用于计算铌样品在制冷机系统中冷却时间的专业工具。该项目提供了直观的GUI界面，支持参数输入、结果分析和图表可视化。

### 功能特性

- 🔧 **参数化计算**: 支持多种系统参数配置
- 📊 **可视化分析**: 提供冷却曲线、热容和热泄漏图表
- 🎨 **双语支持**: 中英文界面切换
- 🏗️ **系统示意图**: 恒温器结构可视化
- ⚡ **多线程计算**: 避免界面冻结
### 技术栈

- **Python 3.8+**
- **tkinter**: GUI框架
- **matplotlib**: 图表绘制
- **numpy**: 数值计算

### 安装运行

#### 1. 环境要求

```bash
Python 3.8+
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 运行程序

**方式一: Python直接运行**
```bash
python cooling_gui.py
```

**方式二: Windows批处理文件**
```bash
start_gui.bat
```

### 项目结构

```
Cryogenic_Cooling_Time_Calculator/
├── README.md                    # 项目说明文档
├── requirements.txt             # Python依赖包列表
├── start_gui.bat               # Windows启动脚本
├── LICENSE                     # MIT许可证
├── cooling_gui.py              # 主GUI应用程序
├── core/                       # 核心计算模块
│   └── calculation_engine.py   # 低温冷却计算引擎
├── utils/                      # 工具模块
│   ├── font_utils.py           # 字体处理工具
│   └── test_utils.py           # 测试工具
├── scripts/                    # 脚本文件
│   ├── simple_calculator.py    # 简化计算器
│   └── test_components.py      # 组件测试脚本
└── docs/                       # 文档文件夹
    ├── README.md               # 详细技术文档
    └── USAGE.md                # 使用指南
```

### 物理模型

#### 德拜模型
- 低温比热容计算
- 材料特性分析

#### 热传导分析
- Stefan-Boltzmann辐射传热
- 残余气体传导
- 多层隔热(MLI)效果

#### 多阶段冷却
- 温度分段计算
- 工程修正系数
- 安全时间估算

### 使用示例

#### 基本参数
- 制冷机功率: 1.0 W
- 真空度: 1×10⁻³ Pa
- 铌样品: 7个 (10cm×2mm×2mm)
- 目标温度: 4.2 K

#### 计算结果
- 理论冷却时间
- 工程估算时间
- 分段详细分析
- 温度-时间曲线

### 贡献指南

欢迎提交Issue和Pull Request来改进项目！

### 许可证

[MIT License](LICENSE)

### 作者信息

**Ming Liu (刘铭)**
- Email: ming-1018@foxmail.com
- Institution: Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences
- GitHub: [@iuming](https://github.com/iuming)

### 更新日志

#### v1.1.0 (2025-07-27)
- 完整的文档系统
- 优化的CI/CD流程
- GitHub Pages自动部署
- 改进的代码质量

#### v1.0.0 (2025-07-27)
- 初始版本发布
- 完整的GUI界面
- 德拜模型计算引擎
- 系统结构示意图
- 双语支持

---

*本项目用于科学研究目的，计算结果仅供参考。*

*This project is for scientific research purposes. Calculation results are for reference only.*