import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--APPLICANTS",
    help="excel with applicants",
    nargs="?",
    const=1,
    default="./applicants_directory/Тестовая база.xlsx",
    type=str,
)
parser.add_argument(
    "--CV_PATH",
    help="path to CVs",
    nargs="?",
    const=1,
    default="./applicants_directory",
    type=str,
)
parser.add_argument(
    "--API_ENDPOINT",
    help="API-endpoint link",
    nargs="?",
    const=1,
    default="https://dev-100-api.huntflow.dev/v2",
    type=str,
)
parser.add_argument("--ACCESS_TOKEN", help="ACCESS_TOKEN", type=str)

terminal_args = parser.parse_args()

API_ENDPOINT = terminal_args.API_ENDPOINT
ACCESS_TOKEN = terminal_args.ACCESS_TOKEN
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
CV_PATH = terminal_args.CV_PATH
APPLICANTS = terminal_args.APPLICANTS
