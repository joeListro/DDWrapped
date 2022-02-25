import datetime
from dateutil import tz
from datadog_api_client.v1 import ApiClient, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.api.notebooks_api import NotebooksApi
from datadog_api_client.v1.api.monitors_api import MonitorsApi

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

Year2022 = datetime.datetime(2022, 1, 1, 0, 0, 0, 0, tzinfo=tz.gettz())

print("Since Jan 1, 2022, you have created:\n------------------------------------")

#Get Number of Dashboards created since the beginning of the year.
count=0
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.list_dashboards(filter_shared=False)

    for dash in response.dashboards:
        if dash.created_at > Year2022:
            # Only add the dashboard to the count if it was created after the new year.
            count+=1

    print(f"{bcolors.OKGREEN}", count, "Dashboards")

#Get Number of Notebooks
count=0
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = NotebooksApi(api_client)
    response = api_instance.list_notebooks()

    for note in response.data:
        if note.attributes.created > Year2022:
            count+=1

    print(f"{bcolors.OKGREEN}", count, "Notebooks")

#Get Number of Monitors
count=0
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.list_monitors()

    for monitor in response:
        if monitor.created > Year2022:
            count+=1

    print(f"{bcolors.OKGREEN}", count, "Monitors")


# Incidents
print(f"{bcolors.HEADER}INCIDENTS")
#Get Number of Incidents
print(f"{bcolors.OKCYAN}You have had X Incidents")
#Get Average time to resolution for Incidents retrieved above.
print(f"{bcolors.OKCYAN}The average time to resolve an incident in Datadog this year was: XX minutes")
