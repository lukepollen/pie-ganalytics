# Set date range to update for each date, based on now()
# cast savefile name from 

"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine
import httplib2
import os
import datetime
import pandas as pd

# Create the SQLAlchemy engine to connect to the database.
engine = create_engine('postgresql://postgres:ve7arut5zaDr@localhost:5432/analytics')

# Create a new table name to create based on the directory path this file is contained in.
absolute_path = os.getcwd()
path_parts = absolute_path.split('\\')
domain_name = path_parts[len(path_parts) -1]
domain_name = domain_name.partition(".")[0]
table_name = domain_name + '_adsense'

# Create table if not exists   
# Importing and creating a list of all distinct start dates and end dates
table_create = "CREATE TABLE " + table_name + ' ' + '(ID SERIAL, index INTEGER, country VARCHAR, metro VARCHAR, devicecategory VARCHAR, medium VARCHAR, source VARCHAR, socialnetwork VARCHAR, year INTEGER, month INTEGER, sessions INTEGER, adsenseecpm FLOAT, adsenserevenue FLOAT, origin VARCHAR);'
start_dates_query = 'SELECT DISTINCT(origin) FROM ' + table_name + ';'
try:
    sql_start_dates = pd.read_sql_query(start_dates_query, engine)
except:
    with engine.connect() as conn:
        conn.execute(table_create)   
    
# Place any dates from an existing table into a start_dates list.
start_dates = []
try:
    for element in sql_start_dates['origin']:
        start_dates.append(element)
except:
    pass

## Importing and creating a list of all distinct start dates and end dates
start_dates = [e.date() for e in pd.to_datetime(start_dates)]
start_dates.sort()
start_date = '2013-06-01'
end_date = datetime.date.today() + datetime.timedelta(- 1) 
full_range = pd.date_range(start_date, end_date).tolist()

# Create list of objects with strftime formatting '%Y-%m-%d' from the dates in start_dates
list_one = []
for e in range(len(start_dates)):
    e = start_dates[e].strftime('%Y-%m-%d')
    list_one.append(e)

# A list of objects with strftime formatting equal to the date range we are interested in. 
list_two = []
for e in range(len(full_range)):
    e = full_range[e].strftime('%Y-%m-%d')
    list_two.append(e)
    
# The difference between the two lists. Sorts after difference determined.
missing_days = [x for x in list_two if x not in list_one]
missing_days.sort()

# Set the origin to the first missing days and print the missing days.
origin = missing_days[0]
#print(missing_days)

def get_service(api_name, api_version, scope, key_file_location,
            service_account_email):
  

    f = open(os.path.expandvars(key_file_location), 'rb')    
    f.close()

    credentials = ServiceAccountCredentials.from_p12_keyfile(
    service_account_email, key_file_location, scopes=scope)

    http = credentials.authorize(httplib2.Http())

  # Build the service object.
    service = build(api_name, api_version, http=http)

    return service
    service = service
    
#3 PauzeRadio

def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
    # Get the first Google Analytics account.
        account = accounts.get('items')[3].get('id')

    # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
        property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
        profiles = service.management().profiles().list(
           accountId=account,
           webPropertyId=property).execute()

    if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[3].get('id')
		
    return None

def get_results(service, profile_id):

  # Date range by Year - Month - Day  
  
  # Use the Analytics Service Object to query the Core Reporting API
    
# Adsense Month by Month
      
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=origin,
      end_date=origin,
      metrics='ga:sessions, ga:adsenseECPM, ga:adsenseRevenue',
      dimensions= 'ga:country, ga:metro, ga:DeviceCategory, ga:medium, ga:source, ga:socialNetwork',
      sort='-ga:sessions', 
      start_index='1',
      max_results='10000000').execute()

def print_results(results):
  
  # Print data table.
    if results.get('rows', []):
        theColumns = ['country', 'metro', 'devicecategory', 'medium', 'source', 'socialnetwork', 'sessions', 'adsenseecpm', 'adsenserevenue', 'origin']
        dataFrame = pd.DataFrame(columns = theColumns)        
    try:
        for row in results.get('rows'):
            theRows = [cell for cell in row]
            theRows.append(origin)        
            dataFrame.loc[len(dataFrame)] = theRows       
    	      # Add the timestamp as a column to the dataframe and then appends this dataframe to the database table
            print(dataFrame)        
            dataFrame.to_sql(table_name, engine, if_exists='append')  
    except:
        print('No Rows!')    
    else:
        print('No Rows Found')        

def main():
  # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
    service_account_email = '588806761212-3bts9vt6t3lrkbj1thhk98sc4simbb6g@developer.gserviceaccount.com'
    key_file_location = 'C:\\Users\\Cortica\\OneDrive - University of Essex\\Luke\\GA API Conversion\\secrets.p12'

  # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location,
        service_account_email)
    profile = get_first_profile_id(service)
    print_results(get_results(service, profile))

if __name__ == '__main__':
    main()

recurring_service = get_service('analytics','v3','https://www.googleapis.com/auth/analytics.readonly','C:\\Users\\Cortica\\OneDrive - University of Essex\\Luke\\GA API Conversion\\secrets.p12','588806761212-3bts9vt6t3lrkbj1thhk98sc4simbb6g@developer.gserviceaccount.com')   
first_profile = get_first_profile_id(recurring_service)
get_results(recurring_service, first_profile)

for e in range(len(missing_days) -1):
    
    origin = missing_days[e + 1]
    results = get_results(recurring_service, first_profile)
    print_results(results)