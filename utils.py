from functools import lru_cache

import requests

from exceptions import UnknownFullNameFormatException


@lru_cache(maxsize=10)
def get_account_id(api_endpoint: str, token: dict) -> int:
    """
    Returns an account id of the current user

    :param api_endpoint: API server link
    :param token: user's access token
    :return: account id
    """
    response = requests.get(
        f"{api_endpoint}/accounts", headers={"Authorization": token}
    )
    response_json = response.json()
    account_id = response_json.get("items")[0].get("id")
    return account_id


def get_first_middle_last_names(name: str) -> list:
    name_parts: list = name.split()
    words_in_fullname = len(name_parts)
    if words_in_fullname == 2:
        name_parts.append(None)
    elif words_in_fullname < 2 or words_in_fullname > 3:
        raise UnknownFullNameFormatException("Unknown name format")
    return name_parts


def pack_applicant_info_into_dict(applicant_dict: dict) -> dict:
    """
    Function packs the raw applicant info into format of a request body

    :param applicant_dict: raw data dict
    :return: request body dict
    """
    body = {
        "last_name": applicant_dict.get("last_name"),
        "first_name": applicant_dict.get("first_name"),
        "middle_name": applicant_dict.get("middle_name"),
        "phone": applicant_dict.get("phone"),
        "email": applicant_dict.get("email"),
        "position": applicant_dict.get("position"),
        "company": applicant_dict.get("company"),
        "money": applicant_dict.get("money"),
        "birthday_day": applicant_dict.get("birthday_day"),
        "birthday_month": applicant_dict.get("birthday_month"),
        "birthday_year": applicant_dict.get("birthday_year"),
        "photo": applicant_dict.get("photo"),
        "externals": [
            {
                "data": {"body": applicant_dict.get("body")},
                "auth_type": applicant_dict.get("auth_type", "NATIVE"),
                "files": applicant_dict.get("file"),
                "account_source": applicant_dict.get("account_source"),
            }
        ],
    }
    return body
