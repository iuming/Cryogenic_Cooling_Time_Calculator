# Cryogenic Cooling Time Calculator

A comprehensive GUI application for calculating cooling time of niobium samples in a 1W cryocooler system.

## Features

- **Interactive GUI**: User-friendly interface with parameter input, results display, and visualization
- **System Schematic**: Built-in cryostat structure diagram with multi-language support
- **Detailed Analysis**: Multi-stage cooling calculation with heat leak modeling
- **Visualization**: Cooling curves, heat capacity plots, and system analysis charts
- **Multi-language**: Supports both Chinese and English interfaces

## System Description

This calculator is designed for a 1W helium cryocooler system cooling 7 niobium samples from 300K to 4.2K:

- **Samples**: 7 niobium pieces (10cm × 2mm × 2mm each)
- **Cryocooler**: 1W nominal cooling power
- **Cold Shield**: Copper, φ1.2m × 1.3m × 5mm thick
- **Copper Plate**: 30cm × 20cm × 3mm for thermal uniformity
- **Insulation**: Multi-layer insulation (50 layers outer + 10 layers inner)
- **Vacuum**: 1×10⁻³ Pa operating pressure

## Installation

### Requirements
```
python >= 3.7
numpy
matplotlib
tkinter (usually included with Python)
```

### Install Dependencies
```bash
pip install numpy matplotlib
```

## Usage

### Quick Start
1. Run the GUI application:
   ```bash
   python cooling_gui.py
   ```
   Or double-click `start_gui.bat` on Windows

2. Adjust parameters in the "参数设置" (Parameter Settings) tab
3. Click "开始计算" (Start Calculation) to run the analysis
4. View results in "计算结果" (Results) and "结果图表" (Charts) tabs

### Parameter Settings

- **System Parameters**: Cooling power, vacuum level, temperature range
- **Sample Parameters**: Number, dimensions of niobium samples
- **Copper Plate**: Dimensions for thermal uniformity
- **Cold Shield**: Dimensions and thermal mass
- **Multi-layer Insulation**: Layer counts for heat leak reduction
- **Calculation Options**: Include/exclude cold shield cooling, liquid nitrogen pre-cooling

### Features

1. **Real-time Calculation**: Multi-threaded processing with progress indication
2. **System Visualization**: Interactive cryostat schematic diagram
3. **Comprehensive Analysis**: Stage-by-stage cooling time breakdown
4. **Engineering Estimates**: Safety factors and practical time ranges
5. **Language Support**: Switch between Chinese and English interfaces

## File Structure

```
Cooling/
├── cooling_gui.py           # Main GUI application
├── core/
│   └── calculation_engine.py  # Core calculation algorithms
├── utils/
│   ├── font_utils.py        # Font handling utilities
│   └── test_utils.py        # Testing utilities
├── scripts/
│   ├── simple_calculator.py # Simplified calculation script
│   └── test_components.py   # Component testing
├── docs/
│   └── README.md           # This file
├── start_gui.bat           # Windows launcher
└── requirements.txt        # Python dependencies
```

## Calculation Method

The cooling time calculation uses a multi-stage approach:

1. **Heat Capacity Modeling**: Temperature-dependent specific heat using Debye model for low temperatures
2. **Heat Leak Analysis**: Radiation, gas conduction, and support conduction
3. **Stage-wise Calculation**: Discretized temperature ranges with average properties
4. **Engineering Corrections**: Safety factors and practical considerations

### Key Physics

- **Materials**: Niobium (samples) and copper (plate, cold shield)
- **Heat Transfer**: Conduction, radiation, and residual gas effects
- **Thermal Insulation**: Multi-layer insulation (MLI) effectiveness
- **System Integration**: Thermal links and temperature distribution

## Results Interpretation

The calculator provides:

- **Cooling Time**: Stage-by-stage and total cooling duration
- **Energy Analysis**: Heat removal requirements for each temperature range
- **Safety Margins**: Conservative estimates with engineering factors
- **Optimization Suggestions**: System improvement recommendations

### Typical Results
- **Without cold shield pre-cooling**: 2-3 days total cooling time
- **With liquid nitrogen pre-cooling**: Significantly reduced time
- **Engineering estimate**: 20-30% longer than theoretical calculation

## Validation

The calculation has been validated against:
- Literature values for material properties
- Experimental data from similar cryogenic systems
- Engineering experience with 1W cryocoolers

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is released under the MIT License. See LICENSE file for details.

## Authors

**Ming Liu (刘铭)**
- 📧 Email: ming-1018@foxmail.com
- 🐙 GitHub: [@iuming](https://github.com/iuming)
- 🏛️ Institution: Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences

## Contact

For questions or support:
- Email: ming-1018@foxmail.com
- Institution: Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences
- GitHub Issues: [Project Issues](https://github.com/iuming/Cryogenic_Cooling_Time_Calculator/issues)

## Acknowledgments

- Key Laboratory of Particle Acceleration Physics and Technology, Chinese Academy of Sciences
- Institute of High Energy Physics (IHEP), Chinese Academy of Sciences
- Cryogenic engineering community for physics models
- Open source Python community for development tools

---

*Last updated: July 2025*
