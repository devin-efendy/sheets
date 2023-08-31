from __future__ import print_function

import os
from dotenv import load_dotenv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
spreadsheet_id = os.getenv('SPREADSHEET_ID')
SAMPLE_RANGE_NAME = '09!D6:F'

CATEGORY_IDX = 0
SUB_CATEGORY_IDX = 1
AMOUNT_IDX = 2


def get_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = get_creds()

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet_service = service.spreadsheets()
        result = sheet_service.values().get(spreadsheetId=spreadsheet_id,
                                            range=SAMPLE_RANGE_NAME).execute()

        sheet = result.get('values')

        sankey = {}  # { category: { sub_category_1: amount, sub_category_2: amount, } }

        for row in sheet:
            category_key = row[CATEGORY_IDX]
            sub_category_key = row[SUB_CATEGORY_IDX]
            amount = row[AMOUNT_IDX]

            category = None

            if category_key not in sankey.keys():
                category = {}
                sankey[category_key] = category
            else:
                category = sankey[category_key]

            if sub_category_key not in category.keys():
                category[sub_category_key] = 0

            category[sub_category_key] += float(amount)

        top_level_str = ""
        output_str = ""

        for category, sub_category in sankey.items():
            total = 0
            for sub, amount in sub_category.items():
                total += amount
                output_str += f"{category} [{amount:.2f}] {sub}\n"
            output_str += "\n"

            # top_level_str += f"Income [{total:.2f}] {category}\n"

        # print(top_level_str)
        print(output_str)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
