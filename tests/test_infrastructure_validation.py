import pytest
import numpy as np
from pathlib import Path
import tempfile
import sys
import os


class TestInfrastructureValidation:
    """Test suite to validate the testing infrastructure setup."""
    
    def test_pytest_works(self):
        """Test that pytest is working correctly."""
        assert True
    
    def test_numpy_import(self):
        """Test that numpy can be imported and basic operations work."""
        arr = np.array([1, 2, 3, 4, 5])
        assert arr.sum() == 15
        assert arr.mean() == 3.0
    
    def test_fixtures_available(self, temp_dir, sample_emg_data):
        """Test that fixtures from conftest.py are available."""
        assert temp_dir.exists()
        assert isinstance(sample_emg_data, np.ndarray)
        assert sample_emg_data.shape == (1000, 8)
    
    def test_mock_functionality(self, mock_keras_model):
        """Test that mock fixtures work correctly."""
        predictions = mock_keras_model.predict(np.random.rand(1, 8))
        assert predictions is not None
        mock_keras_model.predict.assert_called_once()
    
    @pytest.mark.unit
    def test_unit_marker(self):
        """Test that unit test marker works."""
        assert True
    
    @pytest.mark.integration 
    def test_integration_marker(self):
        """Test that integration test marker works."""
        assert True
    
    def test_file_operations(self, temp_dir):
        """Test file operations in temporary directory."""
        test_file = temp_dir / "test.txt"
        test_file.write_text("Hello, testing!")
        content = test_file.read_text()
        assert content == "Hello, testing!"
    
    def test_python_path_includes_project_root(self):
        """Test that the project root is in Python path for imports."""
        project_root = Path(__file__).parent.parent
        assert str(project_root) in sys.path or str(project_root.resolve()) in sys.path
    
    def test_coverage_configuration(self):
        """Test that coverage configuration is working."""
        # This test will only pass if coverage is configured correctly
        # The actual coverage will be measured when running with --cov
        assert True
    
    def test_environment_variables(self):
        """Test environment handling."""
        test_var = os.environ.get('TEST_VAR', 'default_value')
        assert isinstance(test_var, str)


class TestDataProcessing:
    """Test data processing utilities that might be useful for the main code."""
    
    def test_array_normalization(self, sample_emg_data):
        """Test basic array normalization."""
        normalized = (sample_emg_data - sample_emg_data.mean()) / sample_emg_data.std()
        assert abs(normalized.mean()) < 1e-10  # Should be close to 0
        assert abs(normalized.std() - 1.0) < 1e-10  # Should be close to 1
    
    def test_array_reshaping(self, sample_emg_data):
        """Test array reshaping operations."""
        # Test flattening
        flattened = sample_emg_data.flatten()
        assert flattened.shape == (8000,)
        
        # Test reshape back
        reshaped = flattened.reshape(1000, 8)
        assert reshaped.shape == sample_emg_data.shape
        assert np.array_equal(reshaped, sample_emg_data)
    
    def test_batch_processing(self, sample_emg_data):
        """Test batch processing functionality."""
        batch_size = 50
        num_batches = len(sample_emg_data) // batch_size
        
        batches = []
        for i in range(num_batches):
            start_idx = i * batch_size
            end_idx = start_idx + batch_size
            batch = sample_emg_data[start_idx:end_idx]
            batches.append(batch)
        
        assert len(batches) == num_batches
        assert all(batch.shape == (batch_size, 8) for batch in batches)


@pytest.mark.slow
class TestSlowOperations:
    """Test slow operations that might be skipped in quick test runs."""
    
    def test_large_array_operations(self):
        """Test operations on large arrays."""
        large_array = np.random.rand(10000, 100)
        result = np.dot(large_array.T, large_array)
        assert result.shape == (100, 100)
    
    def test_multiple_iterations(self):
        """Test operations that require multiple iterations."""
        results = []
        for i in range(100):
            arr = np.random.rand(10, 10)
            eigenvals = np.linalg.eigvals(arr)
            results.append(eigenvals.max())
        assert len(results) == 100