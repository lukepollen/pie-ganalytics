# pie-ganalytics

![python google analytics adsense earnings by country](https://github.com/lukepollen/pie-ganalytics/blob/development/earningsByCountry.PNG)


# The Project
Google Analytics in the Python environment, using the scientific stack for data exploration and visualisation. Up to seven dimensions of data can be drawn from the API, as opposed to two with the web UI, allowing for a deep analysis of the data, helping you make more money and / or further your plans for world domination. 

![python-google-analytics-traffic-by-channel](https://github.com/lukepollen/pie-ganalytics/blob/development/trafficSourcesVisualisation.PNG)
![python-google-analytics-relative-volumes](https://github.com/lukepollen/ce203AssignmentTwo/blob/master/pacman-clone-luke-pollen-manhattan-distance.PNG)
![python-google-analytics-sessions-by-country-region](https://github.com/lukepollen/ce203AssignmentTwo/blob/master/pacman-clone-luke-pollen-manhattan-distance.PNG)

# Steps

1. ) Create your Project in the Google API Console and retrieve your secrets.p12 file.
2. ) Install Python with the scientific stack (numpy, pands and matplotlib) and these modules dependencies.
3. ) Update the syntax of engine in the initialiseDataFrame function of dataFrameFunctions.py and in the analytics_ .py downloader files to locate your database.
4. ) Change the details in def main() of print_profiles and the analytics_ .py files to your service account email and key file location (the secrets.p12)
5. ) Run print_profiles and record the indices of the property, account and view; for the fourth view of the first account in your fourth property record the indices 3, 0, 3
6. ) Enter these indices in the get_first_profile function of the analytics_ downloaders. Run the downloaders after updating.
7. ) Run the remaining python files to chart, e.g. source.py will chart user activites by your combinations of source, medium, country, region, etc.

Happy insight gathering! 

# Preliminary Setup

The data analysis files will only function if you have created a Project in the Google API Console; a good tutorial to create a project can be found at https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py . Numpy, pandas, matplotlib and their dependencies are also required. I recommend the scientific distribution https://www.anaconda.com/download/ .

Data in your Google Analytics account is downloaded via the python files with the analytics_ prefix. The database table name is determined by the parent folder; if you run analytics_source to obtain user session data for your client, Blue Widgets, in a folder called bluewidgets, the table created will be called bluewidgets_keywords. If you run analytics_adsense in the same folder, the table for your account profile's analytics data will be stored in analytics_adsense. The visualisation files, e.g. adsense, keywords or source will draw data from their respective tables - run the downloaders first.

# Database Identification

It is also necessary to supply the details of the database to write the pandas dataframes created when downloading data from the Google Analytics API by changing the SQLAlchemy engine. This should take the syntax of the following line. Using postgres on the localhost, an example for my connection is provided below:

# Abstract engine example
engine = create_engine('dialect+driver://username:password@host:port/database')
# Actual implementation example
engine = create_engine('postgresql://postgres:password@localhost:5432/analytics')


