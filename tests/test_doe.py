from src.doe import generate_synthetic_doe, process_window


def test_synthetic_doe_has_full_factorial_and_centers():
    config = {"random_state": 7, "center_point_replicates": 3, "factors": {"pressure_mTorr": [20, 60], "rf_power_W": [300, 700], "gas_flow_sccm": [30, 70]}}
    frame = generate_synthetic_doe(config)
    assert len(frame) == 11
    assert (frame["data_origin"] == "synthetic_teaching_demonstration").all()


def test_window_is_boolean():
    config = {"random_state": 7, "center_point_replicates": 1, "factors": {"pressure_mTorr": [20, 60], "rf_power_W": [300, 700], "gas_flow_sccm": [30, 70]}}
    result = process_window(generate_synthetic_doe(config), {"etch_rate_nm_min": [50, 150], "uniformity_percent_max": 10})
    assert result["within_illustrative_window"].dtype == bool
