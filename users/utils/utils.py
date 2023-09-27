import re
from datetime import datetime


def valida_data(data: str) -> bool:
    padrao = r"^\d{2}[-/]\d{2}[-/](?:\d{4}|\d{2})$"

    if re.match(padrao, data):
        print("passou na validacao")
        return True
    else:
        return False


def transform_date(input_date: str) -> str:
    date_obj = datetime.strptime(input_date, "%d-%m-%Y")

    output_date = date_obj.strftime("%Y-%m-%d")

    return output_date


def transform_date_inverse(input_date: str) -> str:
    date_obj = datetime.strptime(input_date, "%Y-%m-%d")

    output_date = date_obj.strftime("%d-%m-%Y")

    return output_date
