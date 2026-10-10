import numpy as np
import pandas as pd
from src.statistical_tests import cohens_d, compare_by_yield


def test_cohens_d_direction_is_explicit():
    assert cohens_d(np.array([3, 4, 5]), np.array([0, 1, 2])) > 0


def test_comparison_returns_bh_adjusted_p_values():
    result = compare_by_yield(pd.DataFrame({"x": [0, 0, 5, 5], "y": [1, 2, 1, 2]}), pd.Series([False, False, True, True]))
    assert "p_value_bh" in result
