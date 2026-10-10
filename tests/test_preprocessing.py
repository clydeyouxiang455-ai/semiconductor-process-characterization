import pandas as pd
from src.preprocessing import select_model_features


def test_removes_constant_and_excessively_missing_columns():
    frame = pd.DataFrame({"usable": [1, 2, 3], "constant": [1, 1, 1], "sparse": [None, None, 3]})
    selected, audit = select_model_features(frame, 0.5)
    assert list(selected) == ["usable"]
    assert audit.set_index("feature").loc["constant", "keep_for_model"] == False
