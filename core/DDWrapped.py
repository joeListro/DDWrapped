from cgi import print_environ_usage
import os
import time
import datetime
from dateutil.parser import parse as dateutil_parser
from dateutil import tz
from datadog_api_client.v1 import ApiClient, ApiException, Configuration
from datadog_api_client.v1.api.dashboards_api import DashboardsApi
from datadog_api_client.v1.api.notebooks_api import NotebooksApi
from datadog_api_client.v1.api.monitors_api import MonitorsApi
from datadog_api_client.v1.api import hosts_api
from datadog_api_client.v1.models import *

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

#Only define the date once for maintainability.
Year = datetime.datetime(2022, 1, 1, 0, 0, 0, 0, tzinfo=tz.gettz())

print(f"{bcolors.UNDERLINE}Since Jan 1, 2022, you have created:{bcolors.ENDC}")

#Get Number of Dashboards created since the beginning of the year.
count=0
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = DashboardsApi(api_client)
    response = api_instance.list_dashboards(filter_shared=False)

    for dash in response.dashboards:
        if dash.created_at > Year:
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
        if note.attributes.created > Year:
            count+=1

    print(f"{bcolors.OKGREEN}", count, "Notebooks")

#Get Number of Monitors
count=0
configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = MonitorsApi(api_client)
    response = api_instance.list_monitors()

    for monitor in response:
        if monitor.created > Year:
            count+=1

    print(f"{bcolors.OKGREEN}", count, "Monitors")

# Hosts
print(f"{bcolors.UNDERLINE}{bcolors.HEADER}HOSTS{bcolors.ENDC}")

configuration = Configuration()
with ApiClient(configuration) as api_client:
    api_instance = hosts_api.HostsApi(api_client)
    _from = 1640995200  # int | Number of seconds from which you want to get total number of active hosts. (optional)
    try:
        # Get the total number of active hosts
        api_response = api_instance.get_host_totals(_from=_from)
        totalHosts=api_response.total_active
        totalUp=api_response.total_up
        print(f"{bcolors.OKBLUE}You have had", totalHosts, "total active hosts.")
        print(f"{bcolors.OKBLUE}You have", totalUp, "total up hosts.")
    except ApiException as e:
        print("Exception when calling HostsApi->get_host_totals: %s\n" % e)

# Incidents
print(f"{bcolors.UNDERLINE}{bcolors.HEADER}INCIDENTS{bcolors.ENDC}")

#Get Number of Incidents

#Incidents use v2 of the api client
from datadog_api_client.v2 import ApiClient, Configuration
from datadog_api_client.v2.api.incidents_api import IncidentsApi

#v2 of the api client generates an unstable operation user warning, ignore it for now
import warnings

#Python program to find the average of an int list
def Average(resTime):
    return sum(resTime) / len(resTime)

count=0
resTime=[]
numIncidents=0
configuration = Configuration()
configuration.unstable_operations["list_incidents"] = True
with ApiClient(configuration) as api_client:
    api_instance = IncidentsApi(api_client)
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        response = api_instance.list_incidents()

    for incident in response.data:
        if incident.attributes.created > Year:
            count+=1
        resTime.append(incident.attributes.time_to_resolve)

    print(f"{bcolors.OKCYAN}You have had", count, "New Incidents")

#Get Average time to resolution for Incidents retrieved above and filter to give a useful metric.
avgTimeMins=Average(resTime)/60
if avgTimeMins > 1000:
    avgTimeHrs=avgTimeMins/60
    if avgTimeHrs > 1000:
        avgTimeDays=avgTimeHrs/12
        print(f"{bcolors.OKCYAN}The average time to resolve an incident in Datadog was:", avgTimeDays, "days")
    else:
        print(f"{bcolors.OKCYAN}The average time to resolve an incident in Datadog was:", avgTimeHrs, "hours")
else:
    print(f"{bcolors.OKCYAN}The average time to resolve an incident in Datadog was:", avgTimeMins, "minutes")