import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app.services import calculate_calories

def test_calculate_calories():
    assert calculate_calories(70, 22) == 1540