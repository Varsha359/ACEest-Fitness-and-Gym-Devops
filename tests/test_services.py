import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services import get_program_details


def test_fat_loss_program():
    result = get_program_details("Fat Loss (FL)")
    assert result is not None
    assert "workout" in result
    assert "diet" in result


def test_invalid_program():
    result = get_program_details("Invalid")
    assert result is None