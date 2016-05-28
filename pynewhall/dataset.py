import json

class Dataset:
    # Holds all the data nessisary to run the model.  Lat/long, elevation,
    # temperature, precip, and hemispheres are the bare minimum needed.
    # Also includes a metadata dictionary should there be optional details
    # to store that are unrelated to model operation.

    def get(self, key):
        return self.ds_dict[key]

    def set(self, key, value):
        if key in self.ds_dict:
            self.ds_dict[key] = value
        else:
            raise Exception("Argument key is not a valid dataset property.")

    def to_dict(self):
        return self.ds_dict

    def to_json(self):
        # Return dataset as JSON string.
        return json.dumps(self.ds_dict, sort_keys=True)

    def __init__(self, input_dict, input_metadata_dict=None):
        # Construct a dataset given input property dictionary.  Optionally specify
        # a metadata dictionary (partial or complete) of properties.

        self.ds_dict = {
            "name": "", 
            "country": "", 
            "latitude": "", 
            "longitude": "", 
            "ns_hemisphere": "",
            "ew_hemisphere": "", 
            "elevation": "", 
            "precipitation": "", 
            "temperature": "", 
            "start_year": "",
            "end_year": "", 
            "is_metric": ""
        }
        
        # Many of these metadata properties are from the USDA's MLRA
        # database, helping with tracking the lifecycle of input data.
        metadata_dict = {
            "station_name": "", 
            "station_id": "", 
            "station_elevation": "", 
            "station_state_providence": "", 
            "station_country": "",
            "mlra_name": "", 
            "mlra_id": "", 
            "contrib_first_name": "",
            "contrib_last_name:": "",
            "contrib_title": "",
            "contrib_org": "",
            "contrib_address": "", 
            "contrib_city": "", 
            "contrib_state_providence": "",
            "contrib_postal": "", 
            "contrib_country": "", 
            "contrib_email": "", 
            "contrib_phone": "",
            "notes": "", 
            "run_date": "", 
            "model_version": "", 
            "unit_system": "", 
            "network": ""
        }

        # Inititalize dictionary from inputs, checking
        # for presence of all keys.
        try:
            # First for the basics.
            for key in self.ds_dict:
                self.ds_dict[key] = input_dict[key]
            # Expand lat/lon from decimal degrees into degrees and minutes.
            # During export only decimal degrees are saved.
            self.ds_dict["latitude_deg"] = int(self.ds_dict["latitude"])
            self.ds_dict["latitude_min"] = \
                (self.ds_dict["latitude"] - self.ds_dict["latitude_deg"]) * 60
            # Also for optional metadata dictionary.
            if input_metadata_dict:
                # Non-critical metadata, treat the missing as empty strings.
                for key in input_metadata_dict:
                    if key in metadata_dict:
                        # Only add anticipated keys.  Override default value.
                        metadata_dict[key] = input_metadata_dict[key]
            self.ds_dict["metadata"] = metadata_dict
        except KeyError as ex:
            raise Exception("Cannot buld dataset, input is missing property: {}".format(ex))

class RunResult:
    # Holds the results of a run of the model.  This includes temperature and moisture
    # calendards, day counts in the moisture control section, USDA regime determination,
    # and so forth.  Also includes the model run inputs so all variables used to generate
    # the results are preserved.

    def get(self, key):
        return self.rr_dict[key]

    def set(self, key, value):
        if key in self.rr_dict:
            self.rr_dict[key] = value
        else:
            raise Exception("Argument key is not a valid dataset property.")

    def to_dict(self):
        composite_dict = self.rr_dict
        composite_dict["dataset"] = self.dataset.to_dict()
        return composite_dict

    def to_json(self):
        # Return dataset as JSON string.
        return json.dumps(self.to_dict, sort_keys=True)

    def get_dataset(self):
        return self.dataset

    def __init__(self, data_set, result_map):
        # Store original dataset, merge in result_map.
        self.dataset = data_set
        self.rr_dict = {
            "annual_rainfall_mm": "",
            "water_holding_capacity_mm": "",
            "annual_water_balance": "",
            "summer_water_balance": "",
            "mean_potential_evapotranspiration": "",
            "days_dry_after_summer_solstice": "",
            "moist_days_after_winter_solstice": "",
            "num_cumulative_days_dry": "",
            "num_cumulative_days_moist_dry": "",
            "num_cumulative_days_moist": "",
            "num_cumulative_days_dry_over_5c": "",
            "num_cumulative_days_moist_dry_over_5c": "",
            "num_cumulative_days_moist_over_5c": "",
            "num_consecutive_days_moist_someplaces": "",
            "num_consecutive_days_moist_over_8c_someplaces": "",
            "temperature_calendar": "",
            "moisture_calendar": "",
            "temperature_regime": "",
            "moisture_regime": "",
            "regime_subdivision_1": "",
            "regime_subdivision_2": "",
            "soil_air_offset_c": "",
            "soil_air_amplitude": ""
        }

        try:
            # Verify all keys are present.
            for key in self.rr_dict:
                self.rr_dict[key] = result_map[key]
        except KeyError as ex:
            raise Exception("Input is missing property: {}".format(ex))
