"""
Unit tests for the Cryogenic Cooling Time Calculator
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import numpy as np
from core.calculation_engine import CryogenicCalculationEngine


class TestCryogenicCalculationEngine:
    """Test cases for the calculation engine"""
    
    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.engine = CryogenicCalculationEngine()
    
    def test_debye_heat_capacity_known_values(self):
        """Test Debye heat capacity calculation with known values"""
        # Test for niobium at 100K (known approximate value)
        result = self.engine.debye_heat_capacity(100, 275)  # T=100K, theta_D=275K
        
        # The result should be positive and reasonable
        assert result > 0
        assert result < 1000  # Reasonable upper bound for heat capacity
        
        # Test at very low temperature (should approach 0)
        low_temp_result = self.engine.debye_heat_capacity(1, 275)
        assert low_temp_result > 0
        assert low_temp_result < result  # Should be less than at 100K
    
    def test_debye_heat_capacity_temperature_dependence(self):
        """Test that heat capacity increases with temperature (generally)"""
        temps = [10, 50, 100, 200]
        theta_d = 275  # Niobium Debye temperature
        
        results = [self.engine.debye_heat_capacity(T, theta_d) for T in temps]
        
        # Generally, heat capacity should increase with temperature
        for i in range(len(results) - 1):
            assert results[i+1] > results[i], f"Heat capacity should increase from {temps[i]}K to {temps[i+1]}K"
    
    def test_debye_heat_capacity_input_validation(self):
        """Test input validation for Debye heat capacity calculation"""
        # Test negative temperature
        with pytest.raises((ValueError, ZeroDivisionError)):
            self.engine.debye_heat_capacity(-10, 275)
        
        # Test zero temperature
        result_zero = self.engine.debye_heat_capacity(0.1, 275)  # Very close to zero
        assert result_zero >= 0
    
    def test_calculate_cooling_time_basic(self):
        """Test basic cooling time calculation"""
        # Basic test parameters
        params = {
            'initial_temp': 300,  # K
            'final_temp': 50,     # K
            'sample_mass': 0.1,   # kg
            'cooling_power': 1.0, # W
            'heat_leak': 0.1      # W
        }
        
        # Calculate cooling time
        result = self.engine.calculate_cooling_time(**params)
        
        # Result should be positive
        assert result > 0
        
        # Result should be reasonable (not too large)
        assert result < 86400  # Less than 24 hours for this simple case
    
    def test_material_properties(self):
        """Test material property constants"""
        # Test that Debye temperatures are reasonable
        assert hasattr(self.engine, 'debye_temperature_nb')
        assert hasattr(self.engine, 'debye_temperature_cu')
        
        # Niobium Debye temperature should be around 275K
        if hasattr(self.engine, 'debye_temperature_nb'):
            assert 250 <= self.engine.debye_temperature_nb <= 300
        
        # Copper Debye temperature should be around 343K
        if hasattr(self.engine, 'debye_temperature_cu'):
            assert 320 <= self.engine.debye_temperature_cu <= 360


class TestPhysicsValidation:
    """Test physics validity and edge cases"""
    
    def setup_method(self):
        self.engine = CryogenicCalculationEngine()
    
    def test_heat_capacity_units(self):
        """Test that heat capacity has correct units (J/kg/K)"""
        result = self.engine.debye_heat_capacity(100, 275)
        
        # For niobium at 100K, typical heat capacity is ~50-200 J/kg/K
        assert 10 <= result <= 500, f"Heat capacity {result} J/kg/K seems unreasonable"
    
    def test_high_temperature_limit(self):
        """Test behavior at high temperatures"""
        # At very high temperatures (T >> theta_D), heat capacity should approach 3R
        high_temp_result = self.engine.debye_heat_capacity(2000, 275)
        
        # Should be positive and finite
        assert np.isfinite(high_temp_result)
        assert high_temp_result > 0


if __name__ == "__main__":
    pytest.main([__file__])
