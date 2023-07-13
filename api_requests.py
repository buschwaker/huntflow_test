import requests
from requests import Response
from requests_toolbelt.multipart.encoder import MultipartEncoder

from decorators import check_status_code
from utils import get_account_id


@check_status_code(200, "File uploading failed")
def post_file(file: str, headers: dict, api_endpoint: str) -> Response:
    """
    Post file and returns Response instance of the request

    :param file: file absolute path
    :param headers: headers of the request
    :param api_endpoint: API server link
    :return: Response instance
    """
    multipart_data = MultipartEncoder(
        fields={
            "file": (file, open(file, "rb"), "text/plain"),
        }
    )
    headers = {**headers, "Content-Type": multipart_data.content_type}
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/upload"
    response = requests.post(url, data=multipart_data, headers=headers)
    return response


@check_status_code(200, "Applicant search failed")
def search_by_last_name(
    last: str, headers: dict, api_endpoint: str
) -> Response:
    """
    Searches an applicant by last name and returns Response instance
    of the request

    :param last: last name of the applicant
    :param headers: headers of the request
    :param api_endpoint: API server link
    :return: Response instance
    """
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/applicants/search?q={last}"
    response = requests.get(url=url, headers=headers)
    return response


@check_status_code(200, "Applicant upload failed")
def upload_applicant(body: dict, headers: dict, api_endpoint: str) -> Response:
    """
    Function uploads an applicant and returns Response instance of the request

    :param body: formatted request body
    :param headers: headers of the request
    :param api_endpoint: API server link
    :return: Response instance
    """
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/applicants"
    response = requests.post(url=url, headers=headers, json=body)
    return response


@check_status_code(200)
def get_or_upload_applicant(
    body: dict, headers: dict, api_endpoint: str
) -> Response:
    """
    Function creates or gets an applicant and returns Response
    instance of the request

    :param body: formatted request body
    :param headers: headers of the request
    :param api_endpoint: API server link
    :return: Response instance
    """
    last = body.get("last_name")
    response_upon_get_applicant = search_by_last_name(
        last, headers, api_endpoint
    )
    applicant_exist = len(response_upon_get_applicant.json().get("items"))
    if applicant_exist:
        response = response_upon_get_applicant
    else:
        response = upload_applicant(body, headers, api_endpoint)
    return response


@check_status_code(200, "Getting vacancies failed")
def get_vacancies(api_endpoint: str, headers: dict) -> Response:
    """
    Returns a Response instance after getting vacancies from the API

    :param api_endpoint: API server link
    :param headers: headers of the request
    :return: Response instance
    """
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/vacancies"
    response = requests.get(url=url, headers=headers)
    return response


@check_status_code(200, "Getting statuses failed")
def get_statuses(api_endpoint: str, headers: dict) -> Response:
    """
    Returns a Response instance after getting statuses from the API

    :param api_endpoint: API server link
    :param headers: headers of the request
    :return: Response instance
    """
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/vacancies/statuses"
    response = requests.get(url=url, headers=headers)
    return response


@check_status_code(200, "Getting rejections failed")
def get_rejection_reasons(api_endpoint: str, headers: dict) -> Response:
    """
    Returns a Response instance after getting rejection reasons from the API

    :param api_endpoint: API server link
    :param headers: headers of the request
    :return: Response instance
    """
    account_id = get_account_id(api_endpoint, headers["Authorization"])
    url = f"{api_endpoint}/accounts/{account_id}/rejection_reasons"
    response = requests.get(url=url, headers=headers)
    return response


@check_status_code(200, "Application upload failed")
def upload_application(
    applicant_data: dict,
    vacancies_ids: dict,
    rejections_ids: dict,
    statuses_ids: dict,
    api_endpoint: str,
    headers: dict,
) -> Response:
    """
    Upload application and returns Response instance of the request

    :param applicant_data: applicant data dict
    :param vacancies_ids: vacancies to ids dictionary
    :param rejections_ids: rejection reasons to ids dictionary
    :param statuses_ids: statuses to ids dictionary
    :param api_endpoint: API server link
    :param headers: headers of the request
    :return: Response instance
    """
    a_id = applicant_data.get("applicant_id")
    status = applicant_data.get("status")
    comment = applicant_data.get("comment")
    file = applicant_data.get("file")
    position = applicant_data.get("position")
    account_id = get_account_id(api_endpoint, headers["Authorization"])

    url = f"{api_endpoint}/accounts/{account_id}/applicants/{a_id}/vacancy"
    json_data = {
        "vacancy": vacancies_ids.get(position),
        "status": statuses_ids.get(status),
        "comment": comment,
        "files": file,
        "rejection_reason": rejections_ids.get(
            comment, rejections_ids["По другой причине"]
        )
        if status == "Отказ"
        else None,
    }

    response = requests.post(url=url, json=json_data, headers=headers)
    return response
