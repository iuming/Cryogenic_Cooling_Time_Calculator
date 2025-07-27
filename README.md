# Cryogenic Cooling Time Calculator

## 项目简介 / Project Overview

低温制冷时间计算器是一个用于计算铌样品在制冷机系统中冷却时间的专业工具。该项目提供了直观的GUI界面，支持参数输入、结果分析和图表可视化。

A professional tool for calculating cooling time of niobium samples in cryocooler systems. This project provides an intuitive GUI interface with parameter input, results analysis, and chart visualization.

[![Python Version](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Documentation](https://img.shields.io/badge/docs-sphinx-blue.svg)](https://iuming.github.io/Cryogenic_Cooling_Time_Calculator/)
[![GitHub Release](https://img.shields.io/github/v/release/iuming/Cryogenic_Cooling_Time_Calculator)](https://github.com/iuming/Cryogenic_Cooling_Time_Calculator/releases)

## 功能特性 / Features

- 🔧 **参数化计算**: 支持多种系统参数配置
- 📊 **可视化分析**: 提供冷却曲线、热容和热泄漏图表
- 🎨 **双语支持**: 中英文界面切换
- 🏗️ **系统示意图**: 恒温器结构可视化
- ⚡ **多线程计算**: 避免界面冻结
- 📋 **详细报告**: 分段分析和工程建议

## 技术栈 / Tech Stack

- **Python 3.12+**
- **tkinter**: GUI框架
- **matplotlib**: 图表绘制
- **numpy**: 数值计算

## 安装运行 / Installation & Usage

### 1. 环境要求 / Requirements

```bash
Python 3.8+
```

### 2. 安装依赖 / Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. 运行程序 / Run Application

**方式一 / Method 1: Python直接运行**
```bash
python cooling_gui.py
```

**方式二 / Method 2: Windows批处理文件**
```bash
start_gui.bat
```

## 项目结构 / Project Structure

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

## 物理模型 / Physics Models

### 德拜模型 / Debye Model
- 低温比热容计算
- 材料特性分析

### 热传导分析 / Heat Transfer Analysis
- Stefan-Boltzmann辐射传热
- 残余气体传导
- 多层隔热(MLI)效果

### 多阶段冷却 / Multi-stage Cooling
- 温度分段计算
- 工程修正系数
- 安全时间估算

## 使用示例 / Usage Examples

### 基本参数 / Basic Parameters
- 制冷机功率: 1.0 W
- 真空度: 1×10⁻³ Pa
- 铌样品: 7个 (10cm×2mm×2mm)
- 目标温度: 4.2 K

### 计算结果 / Calculation Results
- 理论冷却时间
- 工程估算时间
- 分段详细分析
- 温度-时间曲线

## 贡献指南 / Contributing

欢迎提交Issue和Pull Request来改进项目！

Welcome to submit Issues and Pull Requests to improve the project!

## 许可证 / License

[MIT License](LICENSE)

## 作者信息 / Author

**Ming Liu (刘铭)**
- Email: ming-1018@foxmail.com
- Institution: Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences
- GitHub: [@iuming](https://github.com/iuming)

## 更新日志 / Changelog

### v1.0.0 (2025-07-27)
- 初始版本发布
- 完整的GUI界面
- 德拜模型计算引擎
- 系统结构示意图
- 双语支持

---

*本项目用于科学研究目的，计算结果仅供参考。*

*This project is for scientific research purposes. Calculation results are for reference only.*