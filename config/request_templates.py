


class templates:

    operands = {
        "==": "eq",
        ">": "gt",
        "<": "lt",
        ">=": "ge",
        "<=": "le",
        "!=": "ne"
    }

    logical_operators = {
        "AND": " and ",
        "OR": " or "
    }

    base_url = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
    image_base_url = "https://zipper.dataspace.copernicus.eu/odata/v1/Products({product_id})/Nodes"
    filter = "$filter="

    query_by_name = "Name {operand} {value}"
    query_by_collection = "Collection/Name {operand} {value}"
    query_by_publication_date = "PublicationDate {operand} {value}" # ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
    query_by_sensing_date_start = "ContentDate/Start {operand} {value}"
    query_by_sensing_date_end = "ContentDate/End {operand} {value}"
    query_by_polygon = "OData.CSC.Intersects(area=geography'SRID=4326;{polygon_type}({value})')"
    query_by_attribute = "Attributes/OData.CSC.{type}Attribute/any(att:att/Name eq '{attribute_name}' and att/OData.CSC.{type}Attribute/Value {operand} {value})"

    "and PublicationDate lt 2019-05-16T00:00:00.000Z"
    "'SENTINEL-2' and ContentDate/Start gt 2022-05-03T00:00:00.000Z and ContentDate/Start lt 2022-05-03T00:11:00.000Z"
    "$filter=Name eq 'S1A_IW_GRDH_1SDV_20141031T161924_20141031T161949_003076_003856_634E.SAFE'"