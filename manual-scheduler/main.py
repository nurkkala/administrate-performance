from devtools import debug

from data.api_client import PHP_SESSION_ID, BASE_URL
from models.plan import Plan


def main():
    debug(Plan.create_fake_plan())


main()
