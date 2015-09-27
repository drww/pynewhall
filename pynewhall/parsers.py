import json
from model import Dataset

CSV_FIELD_NAMES = ["name", "country", "latitude_degrees", "latitude_minutes", "ns_hemisphere",
        "longitude_degrees", "longitude_minutes", "ew_hemisphere", "elevation", "precipitation",
        "temperature", "start_year", "end_year", "is_metric"]

def csv_parse(contents):
    # Convert raw string CSV format into Dataset.

    # Newline is equivelant to additional field separator.
    contents = contents.replace("\n", ",")
    # Clean out older OS formatting characters.
    contents = contents.replace("\"", "").replace("\r", "")
    # Finally, split.
    field_list = contents.split(",")

    # Assemble dictionary, start with name and country.
    ds_dict = {CSV_FIELD_NAMES[0]: field_list[0],
            CSV_FIELD_NAMES[1]: field_list[1]}

    # Convert latitude into decimal degrees.
    ds_dict["latitude"] = int(field_list[2]) + float(field_list[3]) / 60
    ds_dict[CSV_FIELD_NAMES[4]] = field_list[4]

    # Same with longitude.
    ds_dict["longitude"] = int(field_list[5]) + float(field_list[6]) / 60
    ds_dict[CSV_FIELD_NAMES[7]] = field_list[7]

    # Elevation.
    ds_dict[CSV_FIELD_NAMES[8]] = float(field_list[8]) 

    # Lists of annual precip and temperature (units: C/F, in/mm)
    ds_dict[CSV_FIELD_NAMES[9]] = []
    for field in field_list[9:21]:
        # Explicitly parse precip as floating point.
        ds_dict[CSV_FIELD_NAMES[9]].append(float(field))
    ds_dict[CSV_FIELD_NAMES[10]] = []
    for field in field_list[21:33]:
        # Explicitly parse temperature as well.
        ds_dict[CSV_FIELD_NAMES[10]].append(float(field))

    # Years covered in average by dataset.
    ds_dict[CSV_FIELD_NAMES[11]] = field_list[33]
    ds_dict[CSV_FIELD_NAMES[12]] = field_list[34]

    if field_list[35].upper() == "M":
        # Metric unitsystem for dataset.
        ds_dict[CSV_FIELD_NAMES[13]] = True
    else:
        ds_dict[CSV_FIELD_NAMES[13]] = False

    # Construct and return Dataset object without metadata.
    return Dataset(ds_dict)

def json_parse(contents):
    # Parse JSON, which is super-easy since it maps directly.
    input_dict = json.loads(contents)
    return Dataset(input_dict)

def parse(file):
    # Take input file, apply correct parser, return Dataset.
    contents = file.read()

    # First bytes check.  Classic CSV starts with a string,
    # XML begins with "<?xml", JSON starts with "{".
    first_bytes = contents[0:5]

    if "<?xml" in first_bytes:
        # Use XML parser.
        print "IMPLEMENT XML"
        pass
    elif first_bytes[0] == "{":
        # Use JSON parser.
        return json_parse(contents)
    else:
        # Use CSV parser.
        return csv_parse(contents)
