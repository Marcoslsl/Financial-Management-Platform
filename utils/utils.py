import re
from datetime import datetime


def valida_data(data: str) -> bool:
    padrao = r"^\d{2}[-/]\d{2}[-/](?:\d{4}|\d{2})$"

    if re.match(padrao, data):
        return True
    else:
        return False


def parse_date(input_date: str):
    if "-" in input_date:
        date_obj = datetime.strptime(input_date, "%d-%m-%Y")
    elif "/" in input_date:
        input_date = input_date.replace("/", "-")
        date_obj = datetime.strptime(input_date, "%d-%m-%Y")
    else:
        raise ValueError(
            "Formato de data inválido. Use dd-mm-yyyy ou dd/mm/yyyy."
        )
    return date_obj


def transform_date(input_date: str) -> str:
    date_obj = parse_date(input_date)
    output_date = date_obj.strftime("%Y-%m-%d")
    return output_date


def transform_date_inverse(input_date: str) -> str:
    date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    output_date = date_obj.strftime("%d-%m-%Y")

    return output_date
