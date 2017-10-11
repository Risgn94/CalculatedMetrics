"""A simple example of how to access the Google Analytics API."""

import argparse
from googleapiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
from datetime import timedelta, datetime

class init():
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.DISCOVERY_URI = ('https://analyticsreporting.googleapis.com/$discovery/rest')
        self.CLIENT_SECRETS_PATH = 'client_secrets.json'  # Path to client_secrets.json file.

        """Initializes the analyticsreporting service object.

        Returns:
        analytics an authorized analyticsreporting service object.
        """
        # Parse command-line arguments.
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            parents=[tools.argparser])
        flags = parser.parse_args([])

        # Set up a Flow object to be used if we need to authenticate.
        flow = client.flow_from_clientsecrets(
            self.CLIENT_SECRETS_PATH, scope=self.SCOPES,
            message=tools.message_if_missing(self.CLIENT_SECRETS_PATH))

        # Prepare credentials, and authorize HTTP object with them.
        # If the credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # credentials will get written back to a file.
        storage = file.Storage('analyticsreporting.dat')
        credentials = storage.get()
        if credentials is None or credentials.invalid:
            credentials = tools.run_flow(flow, storage, flags)
        http = credentials.authorize(http=httplib2.Http())

        # Build the service object.
        analytics = build('analytics', 'v4', http=http, discoveryServiceUrl=self.DISCOVERY_URI)
        self._analytics = analytics

    def get_sessions_30_days_total(self, view_Id):
        return self.return_response(self._analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': view_Id,
                        'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'yesterday'}],
                        'metrics': [
                            {'expression': 'ga:sessions'},
                            {'expression': 'ga:adClicks'}
                        ],
                        "metricFilterClauses": [{
                            "filters": [{
                                "metricName": "ga:sessions",
                                "operator": "GREATER_THAN",
                                "comparisonValue": "0"
                            }]
                        }],
                        "orderBys": [
                            {"fieldName": "ga:sessions", "sortOrder": "DESCENDING"},
                        ],
                        'dimensions': [
                            {"name": "ga:sourceMedium"},
                            {"name": "ga:date"},
                            {"name": "ga:adDistributionNetwork"}
                        ]
                    }
                ]
            }
        ).execute())

    def return_response(self, response):
        """Parses and prints the Analytics Reporting API V4 response"""
        return_Values = []
        for report in response.get('reports', []):
            columnHeader = report.get('columnHeader', {})
            metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
            rows = report.get('data', {}).get('rows', [])

            for row in rows:
                dimensions = row.get('dimensions', [])
                dateRangeValues = row.get('metrics', [])

                for i, values in enumerate(dateRangeValues):
                    for metricHeader, value in zip(metricHeaders, values.get('values')):
                        name = metricHeader.get('name')
                        return_Values.append({'dimension': dimensions, 'name': name, 'value': value})

        return return_Values