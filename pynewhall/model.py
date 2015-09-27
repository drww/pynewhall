import json

class Dataset:

    def get_properties(self):
        return self.properties

    def get(self, key):
        return self.ds_dict[key]

    def set(self, key, value):
        if key in self.properties:
            self.ds_dict[key] = value
        else:
            raise Exception("Argument key is not a valid dataset property.")

    def to_dict(self):
        return self.ds_dict

    def to_json(self):
        # Return dataset as JSON string.
        return json.dumps(self.ds_dict, sort_keys=True)

    def __init__(self, input_dict, metadata_dict=None):
        # Construct a dataset given input property dictionary.  Optionally specify
        # a metadata dictionary (partial or complete) of properties.

        self.properties = ["name", "country", "latitude", "longitude", "ns_hemisphere",
                "ew_hemisphere", "elevation", "precipitation", "temperature", "start_year",
                "end_year", "is_metric"]
        self.extended_properties = ["station_name", "station_id", "station_elevation", 
            "station_state_providence", "station_country", "mlra_name", "mlra_id", 
            "contrib_first_name", "contrib_last_name", "contrib_title", "contrib_org",
            "contrib_address", "contrib_city", "contrib_state_providence",
            "contrib_postal", "contrib_country", "contrib_email", "contrib_phone",
            "notes", "run_date", "model_version", "unit_system", "soil_air_offset",
            "amplitude", "network"]
        self.ds_dict = {}

        try:
            # Assemble local dictionary and raise exception on missing keys.
            # These values must be present for model to function.
            for key in self.properties:
                self.ds_dict[key] = input_dict[key]
            if metadata_dict:
                # Non-critical metadata, treat the missing as empty strings.
                for key in self.extended_properties:
                    if key in metadata_dict:
                        self.ds_dict[key] = metadata_dict[key]
                    else:
                        # Record an empty value for the key.
                        self.ds_dict[key] = ""
        except KeyError as ex:
            raise Exception("Input is missing property: {}".format(ex))
