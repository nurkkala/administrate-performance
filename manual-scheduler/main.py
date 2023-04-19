from devtools import debug

from models.plan import Plan


def main():
    debug(Plan.create_fake_plan())


main()
