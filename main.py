from glob import glob
import re

import pandas as pd

from api_requests import (
    get_or_upload_applicant,
    get_statuses,
    get_rejection_reasons,
    get_vacancies,
    post_file,
    upload_application,
)
from args_parser import API_ENDPOINT, APPLICANTS, CV_PATH, HEADERS
from exceptions import (
    NoConnectionException,
    RawHasEmptyCellException,
    UnknownFullNameFormatException,
)
from logger import logger
from utils import get_first_middle_last_names, pack_applicant_info_into_dict
from validators import validate_raw_from_excel


pd.set_option("display.max_columns", None)


def main():
    """Entrypoint"""

    # put info from excel into dataframe
    df = pd.read_excel(APPLICANTS, na_values="NA")
    df.rename(
        columns={
            "Должность": "position",
            "ФИО": "fullname",
            "Ожидания по ЗП": "money",
            "Комментарий": "comment",
            "Статус": "status",
        },
        inplace=True,
    )

    # collecting vacancies, statuses and rejections mappings with ids
    vacancies_dict = {
        item["position"]: item["id"]
        for item in get_vacancies(API_ENDPOINT, HEADERS).json().get("items")
    }
    statuses_dict = {
        item["name"]: item["id"]
        for item in get_statuses(API_ENDPOINT, HEADERS).json().get("items")
    }
    rejection_dict = {
        item["name"]: item["id"]
        for item in get_rejection_reasons(API_ENDPOINT, HEADERS)
        .json()
        .get("items")
    }

    for i in range(len(df)):
        # data extraction from dataframe
        position = df.loc[i, "position"].strip()
        fullname = df.loc[i, "fullname"].strip()
        comment = df.loc[i, "comment"].strip()
        status = df.loc[i, "status"].strip()
        money = "".join(re.findall(r"\d+", str(df.loc[i, "money"])))
        validate_raw_from_excel(df.loc[i])
        last_name, first_name, middle_name = get_first_middle_last_names(
            fullname
        )

        # file uploading
        file = glob(f"{CV_PATH}/{position}/{fullname}*")[0]
        response_cv_to_upload = post_file(file, HEADERS, API_ENDPOINT).json()

        # preparation data for applicant uploading
        file_id = response_cv_to_upload.get("id")
        applicant_data_dict = {
            "position": position,
            "first_name": first_name,
            "last_name": last_name,
            "middle_name": middle_name,
            "file": [file_id],
            "money": money,
            "status": status,
            "comment": comment,
        }
        body_upload_applicant = pack_applicant_info_into_dict(
            applicant_data_dict
        )

        # applicant uploading or retrieve if already exists
        response_applicant = get_or_upload_applicant(
            body_upload_applicant, HEADERS, API_ENDPOINT
        ).json()

        # data preparation for application uploading
        applicant_id = (
            response_applicant.get("id")
            if response_applicant.get("id")
            else response_applicant.get("items")[0].get("id")
        )
        applicant_data_dict.update({"applicant_id": applicant_id})

        # application uploading
        upload_application(
            applicant_data_dict,
            vacancies_dict,
            rejection_dict,
            statuses_dict,
            API_ENDPOINT,
            HEADERS,
        )


if __name__ == "__main__":
    try:
        main()
    except (
        NoConnectionException,
        RawHasEmptyCellException,
        UnknownFullNameFormatException,
    ) as e:
        logger.error(e)
