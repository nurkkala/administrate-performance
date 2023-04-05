import httpx
from devtools import debug

from data.api_client import PHP_SESSION_ID, BASE_URL
from models.location import Country, read_companies, Region, RegionCreateInput


def sandbox(client):
    # delete_resource_type(client, 12)
    # create_resource_type(client, "Climbing Rope", "For Climbing")
    # read_resource_types(client)
    # create_resource(client, "Smart Board", "UmVzb3VyY2VUeXBlOjM=")
    # read_resources(client)
    # read_resource_types(client)
    # read_course_templates(client)
    # read_instructors(client)

    # create_contact(client, "T3JnYW5pc2F0aW9uOjE=", "Wanda", "Montana")
    # read_contacts(client)

    # create_account(client, "Mo Bilhome")
    # read_accounts(client)

    # rtn = create_plan(client,
    #                   PlanCreateInput(name=fake.sentence(),
    #                                   start=datetime(year=2023, month=6, day=3, hour=9),
    #                                   end=datetime(year=2023, month=6, day=7, hour=17),
    #                                   days=["monday", "wednesday", "friday"],
    #                                   startTime=time(hour=9),
    #                                   endTime=time(hour=17),
    #                                   locationId="TG9jYXRpb246Nzk="))
    # new_plan = rtn["plan"]
    # print(b64decode(new_plan.id))
    #
    # debug(new_plan)
    # debug(new_plan.schema())

    # add_instructors_to_plan(client, "UGxhbjo1", ["UGVyc29uOjQz", "UGVyc29uOjQy"])
    # read_plans_list(client)
    pass


def main():
    with httpx.Client(base_url=BASE_URL, cookies={"PHPSESSID": PHP_SESSION_ID}) as client:
        # create_fake_plan(client)
        # debug(read_countries(client))
        # debug(read_companies(client))

        region = Region.fake_region(client)
        debug(region)

        # debug(read_regions(client))
        # debug(Country.read_random_country(client))


main()
