# Contributing to Cryogenic Cooling Time Calculator

Thank you for your interest in contributing to this project! 🎉

## How to Contribute

### 🐛 Reporting Bugs
- Use the [GitHub Issues](https://github.com/iuming/Cryogenic_Cooling_Time_Calculator/issues) page
- Include detailed description and steps to reproduce
- Provide system information (OS, Python version)

### 💡 Suggesting Features
- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Include mockups or examples if applicable

### 🔧 Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/Cryogenic_Cooling_Time_Calculator.git
   cd Cryogenic_Cooling_Time_Calculator
   ```

2. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"  # Install with development dependencies
   ```

3. **Run Tests**
   ```bash
   python -m pytest scripts/ utils/
   ```

4. **Code Style**
   ```bash
   black .                 # Format code
   flake8 .               # Check style
   isort .                # Sort imports
   ```

### 📝 Code Guidelines

- **Python Style**: Follow PEP 8, use Black formatter
- **Line Length**: Maximum 127 characters
- **Documentation**: Add docstrings for all functions
- **Type Hints**: Use type annotations where applicable
- **Comments**: Write clear, concise comments

### 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting
- Test on multiple Python versions (3.8-3.12)
- Test GUI functionality manually

### 📚 Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update CHANGELOG.md with changes
- Include usage examples

### 🚀 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Changes**
   - Follow code guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test Your Changes**
   ```bash
   python cooling_gui.py  # Test GUI
   python -m pytest      # Run tests
   black .               # Format code
   flake8 .             # Check style
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   git push origin feature/your-feature-name
   ```

5. **Open Pull Request**
   - Use descriptive title and description
   - Reference related issues
   - Include screenshots for UI changes

### 🏷️ Commit Message Guidelines

Use conventional commits format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code formatting
- `refactor:` - Code restructuring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

Examples:
```
feat: add temperature unit conversion
fix: resolve Unicode encoding issue in workflows
docs: update installation instructions
```

### 🔬 Physics and Mathematics

When contributing to physics calculations:
- Provide scientific references
- Include unit tests with known values
- Document assumptions and limitations
- Validate against experimental data when possible

### 📞 Getting Help

- Open an issue for questions
- Check existing documentation
- Contact: ming-1018@foxmail.com

### 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

## 中文贡献指南

### 🐛 报告问题
- 使用 [GitHub Issues](https://github.com/iuming/Cryogenic_Cooling_Time_Calculator/issues)
- 包含详细描述和重现步骤
- 提供系统信息（操作系统、Python版本）

### 💡 建议功能
- 使用"enhancement"标签开启issue
- 描述功能及其好处
- 如适用，包含模型图或示例

### 🔧 开发环境设置

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/Cryogenic_Cooling_Time_Calculator.git
   cd Cryogenic_Cooling_Time_Calculator
   ```

2. **安装依赖**
   ```bash
   pip install -e ".[dev]"
   ```

3. **运行测试**
   ```bash
   python -m pytest scripts/ utils/
   ```

感谢您的贡献！🙏
