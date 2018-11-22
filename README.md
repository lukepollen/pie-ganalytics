# pie-ganalytics
Google Analytics in the Python environment, using the scientific stack for data exploration and visualisation. Up to seven dimensions of data can be drawn from the API, as opposed to two with the web UI, allowing for a deep analysis of the data, helping you make more money and / or further your plans for world domination. 

The data analysis files will only function if you have created a Project in the Google API Console; a good tutorial to create a project can be found at https://developers.google.com/analytics/devguides/reporting/core/v4/quickstart/service-py . Numpy, pandas, matplotlib and their dependencies are also required. I recommend the scientific distribution https://www.anaconda.com/download/ .

Data in your Google Analytics account is downloaded via the python files with the analytics_ prefix. The database table name is determined by the parent folder; if you run analytics_source to obtain user session data for your client, Blue Widgets, in a folder called bluewidgets, the table created will be called bluewidgets_keywords. If you run analytics_adsense in the same folder, the table for your account profile's analytics data will be stored in analytics_adsense. The visualisation files, e.g. adsense, keywords or source will draw data from their respective tables - run the downloaders first.

It is also necessary to supply the details of the database to write the pandas dataframes created when downloading data from the Google Analytics API by changing the SQLAlchemy engine. This should take the syntax of the following line. Using postgres on the localhost, an example for my connection is provided below:

# Abstract engine example
engine = create_engine('dialect+driver://username:password@host:port/database')
# Actual implementation example
engine = create_engine('postgresql://postgres:ve7arut5zaDr@localhost:5432/analytics')

Modify the function initializeDataFrame in dataFrameFunctions.py with your database string for the visualisation files to plot the gathered data. Happy insight gathering! 
