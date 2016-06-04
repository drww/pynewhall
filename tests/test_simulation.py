from pynewhall.model import Dataset
from pynewhall.simulation import run_simulation

# Nose tests for simulation component.  Invoke using
# the "nosetests" command in the root of the project
# directory (where the tests/ folder is).

# Compare RunResult dicts to verify results align with expectations.
def compare_results(test_results, expected_results):
    clean_run = True
    for attribute in expected_results.keys():
        if test_results[attribute] != expected_results[attribute]:
            # A property does not match, report and continue.
            print "Property does not match: {} = {} (should be: {})".format(attribute, 
                test_results[attribute], expected_results[attribute])
            clean_run = False
    # Report if the test passed.
    return clean_run

# All tests performed with default WHC, FC, and FCD.  Reference
# is Java Newhall v1.6.1, which is a faithful reimplementation
# of the original Wambeke BASIC version.

def test_mead89():
    # Perform a test of the MEAD89 dataset.
    dataset_dict = {
        "name": "Mead Agronomy Lab",
        "country": "USA", 
        "elevation": 1180.0,
        "start_year": "1989",
        "end_year": "1989",
        "ew_hemisphere": "W",
        "is_metric": False,
        "latitude": 41.166666666666664,
        "longitude": 96.41666666666667,
        "ns_hemisphere": "N", 
        "precipitation": [0.8, 0.46, 0.06, 0.99, 4.08, 4.14, 3.26, 1.62, 2.94, 0.85, 0.05, 0.66], 
        "temperature": [32.0, 15.0, 37.0, 55.0, 63.0, 69.0, 76.0, 73.0, 63.0, 54.0, 36.0, 17.0]
    }

    test_ds = Dataset(dataset_dict)
    test_results = run_simulation(test_ds).to_dict()

    # Enforce that results match against this profile.
    expected_results = {
        "moisture_regime": "Ustic",
        "temperature_regime": "Mesic",
        "annual_rainfall_mm": 505.7,
        "num_cumulative_days_dry": 49,
        "num_cumulative_days_moist_dry": 311,
        "num_cumulative_days_moist": 0,
        "num_cumulative_days_dry_over_5c": 49,
        "num_cumulative_days_moist_dry_over_5c": 166,
        "num_cumulative_days_moist_over_5c": 0,
        "num_consecutive_days_moist_someplaces": 297,
        "num_consecutive_days_moist_over_8c_someplaces": 88,
        "days_dry_after_summer_solstice": 46,
        "moist_days_after_winter_solstice": 0,
        "mean_potential_evapotranspiration": [0.0, 0.0, 7.4, 58.2, 96.6, 122.5, 
            154.7, 132.2, 80.4, 47.5, 4.4, 0.0]
    }

    # Report true/false on comparison of results and expectations.
    assert compare_results(test_results, expected_results)

def test_column97():
    # Perform a test of the Column97 dataset.
    dataset_dict = {
        "name": "Columbus 3 NE",
        "country": "USA", 
        "elevation": 441.96,
        "start_year": "1997",
        "end_year": "1997",
        "ew_hemisphere": "W",
        "is_metric": True,
        "latitude": 41.4666,
        "longitude": 97.3333,
        "ns_hemisphere": "N", 
        "precipitation": [7.6, 19.8, 4.1, 81.8, 86.9, 97.8, 116.6, 55.1, 103.6, 79.5, 3.9, 9.9], 
        "temperature": [-5.0, -1.7, 3.9, 6.1, 12.8, 20.0, 23.3, 21.7, 18.3, 10.6, 1.7, -1.7]
    }

    test_ds = Dataset(dataset_dict)
    test_results = run_simulation(test_ds).to_dict()

    # Enforce that results match against this profile.
    expected_results = {
        "moisture_regime": "Udic",
        "temperature_regime": "Mesic",
        "annual_rainfall_mm": 666.6,
        "num_cumulative_days_dry": 0,
        "num_cumulative_days_moist_dry": 0,
        "num_cumulative_days_moist": 360,
        "num_cumulative_days_dry_over_5c": 0,
        "num_cumulative_days_moist_dry_over_5c": 0,
        "num_cumulative_days_moist_over_5c": 203,
        "num_consecutive_days_moist_someplaces": 360,
        "num_consecutive_days_moist_over_8c_someplaces": 181,
        "days_dry_after_summer_solstice": 0,
        "moist_days_after_winter_solstice": 120,
        "mean_potential_evapotranspiration": [0.0, 0.0, 14.2, 26.0, 71.0, 121.9, 147.4, 126.9,
            90.5, 43.5, 4.2, 0.0]
    }

    # Report true/false on comparison of results and expectations.
    assert compare_results(test_results, expected_results)

def test_column98():
    # Perform a test of the Column98 dataset.
    dataset_dict = {
        "name": "Columbus 3 NE",
        "country": "USA", 
        "elevation": 441.96,
        "start_year": "1998",
        "end_year": "1998",
        "ew_hemisphere": "W",
        "is_metric": True,
        "latitude": 41.4666,
        "longitude": 97.3333,
        "ns_hemisphere": "N", 
        "precipitation": [17.0, 11.2, 73.4, 90.7, 64.5, 183.6, 86.6, 84.3, 28.4, 68.1, 28.4, 6.4], 
        "temperature": [-2.8, 1.7, -0.6, 8.3, 16.1, 17.8, 24.4, 23.3, 21.1, 10.6, 5.0, -1.1]
    }

    test_ds = Dataset(dataset_dict)
    test_results = run_simulation(test_ds).to_dict()

    # Enforce that results match against this profile.
    expected_results = {
        "moisture_regime": "Udic",
        "temperature_regime": "Mesic",
        "annual_rainfall_mm": 742.6,
        "num_cumulative_days_dry": 0,
        "num_cumulative_days_moist_dry": 24,
        "num_cumulative_days_moist": 336,
        "num_cumulative_days_dry_over_5c": 0,
        "num_cumulative_days_moist_dry_over_5c": 24,
        "num_cumulative_days_moist_over_5c": 188,
        "num_consecutive_days_moist_someplaces": 360,
        "num_consecutive_days_moist_over_8c_someplaces": 196,
        "days_dry_after_summer_solstice": 0,
        "moist_days_after_winter_solstice": 120,
        "mean_potential_evapotranspiration": [0.0, 3.4, 0.0, 34.4, 89.8, 102.8, 154.7, 
            136.7, 105.3, 40.6, 13.3, 0.0]
    }

    # Report true/false on comparison of results and expectations.
    assert compare_results(test_results, expected_results)

def test_ajo20008():
    # Perform a test of the Ajo20008 dataset.
    dataset_dict = {
        "name": "Ajo, AZ",
        "country": "USA", 
        "elevation": 549.0,
        "start_year": "1971",
        "end_year": "2000",
        "ew_hemisphere": "E",
        "is_metric": True,
        "latitude": 32.37,
        "longitude": -112.87,
        "ns_hemisphere": "N", 
        "precipitation": [17.02, 17.02, 19.3, 5.84, 3.81, 1.27, 19.3, 41.15, 20.83, 16.0, 12.7, 22.35], 
        "temperature": [12.5, 14.61, 16.78, 20.56, 24.78, 30.06, 32.17, 31.44, 29.33, 23.89, 17.22, 12.61]
    }

    test_ds = Dataset(dataset_dict)
    test_results = run_simulation(test_ds).to_dict()

    # Enforce that results match against this profile.
    expected_results = {
        "moisture_regime": "Aridic",
        "temperature_regime": "Hyperthermic",
        "annual_rainfall_mm": 196.6,
        "num_cumulative_days_dry": 360,
        "num_cumulative_days_moist_dry": 0,
        "num_cumulative_days_moist": 0,
        "num_cumulative_days_dry_over_5c": 360,
        "num_cumulative_days_moist_dry_over_5c": 0,
        "num_cumulative_days_moist_over_5c": 0,
        "num_consecutive_days_moist_someplaces": 0,
        "num_consecutive_days_moist_over_8c_someplaces": 0,
        "days_dry_after_summer_solstice": 120,
        "moist_days_after_winter_solstice": 0,
        "mean_potential_evapotranspiration": [16.3, 23.8, 41.3, 74.4, 135.0, 192.9,
            209.5, 193.2, 160.1, 100.9, 37.8, 16.3]
    }

    # Report true/false on comparison of results and expectations.
    assert compare_results(test_results, expected_results)
