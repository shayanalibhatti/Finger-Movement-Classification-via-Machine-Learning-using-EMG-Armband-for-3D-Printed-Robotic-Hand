import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, MagicMock
import numpy as np


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    temp_path = tempfile.mkdtemp()
    yield Path(temp_path)
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_emg_data():
    """Provide sample EMG data for testing."""
    return np.random.randint(-128, 128, size=(1000, 8))


@pytest.fixture
def mock_myo_device():
    """Mock Myo device for testing."""
    mock_device = Mock()
    mock_device.stream_emg = Mock()
    return mock_device


@pytest.fixture
def mock_myo_hub():
    """Mock Myo Hub for testing."""
    mock_hub = Mock()
    mock_hub.run = Mock()
    return mock_hub


@pytest.fixture
def mock_keras_model():
    """Mock Keras model for testing."""
    mock_model = Mock()
    mock_model.predict = Mock(return_value=np.array([[0.1, 0.8, 0.05, 0.03, 0.02]]))
    mock_model.fit = Mock()
    mock_model.save = Mock()
    return mock_model


@pytest.fixture
def mock_serial_port():
    """Mock serial port for testing."""
    mock_port = Mock()
    mock_port.write = Mock()
    mock_port.readline = Mock(return_value=b'0')
    mock_port.close = Mock()
    mock_port.in_waiting = 1
    return mock_port


@pytest.fixture
def sample_training_labels():
    """Provide sample training labels."""
    return np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4])


@pytest.fixture
def sample_concatenated_array():
    """Provide sample concatenated array for training."""
    return np.random.rand(100, 8)


@pytest.fixture
def mock_matplotlib_plt():
    """Mock matplotlib pyplot for testing."""
    mock_plt = Mock()
    mock_plt.plot = Mock()
    mock_plt.title = Mock()
    mock_plt.xlabel = Mock()
    mock_plt.ylabel = Mock()
    mock_plt.legend = Mock()
    mock_plt.show = Mock()
    return mock_plt


@pytest.fixture(autouse=True)
def disable_user_input(monkeypatch):
    """Automatically disable user input for all tests."""
    monkeypatch.setattr('builtins.input', lambda _: 'test_user')


@pytest.fixture
def mock_process_manager():
    """Mock process management utilities."""
    mock_manager = Mock()
    mock_manager.check_if_process_running = Mock(return_value=True)
    mock_manager.restart_process = Mock(return_value=True)
    return mock_manager


@pytest.fixture
def sample_model_history():
    """Provide sample training history for testing."""
    return {
        'acc': [0.1, 0.3, 0.5, 0.7, 0.9],
        'val_acc': [0.15, 0.35, 0.45, 0.65, 0.85],
        'loss': [2.0, 1.5, 1.0, 0.5, 0.2],
        'val_loss': [1.9, 1.6, 1.2, 0.7, 0.3]
    }