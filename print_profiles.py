# print profiles

# Set date range to update for each date, based on now()
# cast savefile name from 

"""A simple example of how to access the Google Analytics API."""

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import httplib2
import os

targetAccount = 3
targetProperty = 0
targetProfile = 3

def get_service(api_name, api_version, scope, key_file_location,
            service_account_email):
  

    f = open(os.path.expandvars(key_file_location), 'rb')
    key = f.read()
    f.close()

    credentials = ServiceAccountCredentials.from_p12_keyfile(service_account_email, key_file_location, scopes=scope)

    http = credentials.authorize(httplib2.Http())

    # Build the service object.
    service = build(api_name, api_version, http=http)

    return service
    service = service
    
def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    theAccounts = []

    if accounts.get('items'):
        for e in accounts.get('items'):
	        theAccounts.append(e['name'])
        account = accounts.get('items')[targetAccount].get('id')
        print('ACCOUNTS:')
        for e in theAccounts:
	        print('\n' + e)
	
    # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
            accountId=account).execute()

    theProperties = []

    if properties.get('items'):
        for e in properties.get('items'):
            theProperties.append(e['name'])
    property = properties.get('items')[targetProperty].get('id')

    print('\n' + 'PROPERTIES:')
    for e in theProperties:
        print('\n' + e)

      # Get a list of all views (profiles) for the first property.
        profiles = service.management().profiles().list(
           accountId=account,
           webPropertyId=property).execute()

        #~ for e in profiles:
		#~ print '\n' + e

    names = []

    if profiles.get('items'):
        for e in profiles.get('items'):
            names.append(e['name'])
		
        print('\n' + 'PROFILES:')
    for e in names:
        print('\n' + e)
        
    print("\n" + "Target Account : " + theAccounts[targetAccount] + "\n" + "Target Property: " + theProperties[targetProperty] + "\n" + "Target Profile: " + names[targetProfile])
		
    return None

def print_results(results):
  
    print('Profile Name: %s' % results.get('profileInfo').get('profileName'))

     
def main():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    service_account_email = '588806761212-3bts9vt6t3lrkbj1thhk98sc4simbb6g@developer.gserviceaccount.com'
    key_file_location = 'C:\\Backup\\Luke\\GA API Conversion\\secrets.p12'

    # Authenticate and construct service.
    service = get_service('analytics', 'v3', scope, key_file_location,
        service_account_email)
    profile = get_first_profile_id(service)
    #print_results(service, profile)

if __name__ == '__main__':
    main()


