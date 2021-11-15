import unittest
from misc.thumbtack_conn import create_test_data, thumbtack_lead_json_to_list, thumbtack_message_json_to_list, test_thumbtack_send_message

test_lead_dict = {
    "leadID": "437282430869512192",
    "createTimestamp": "1636428031",
    "price": "More information needed to give an estimate",
    "request": {
        "requestID": "437282427823792129",
        "category": "House Cleaning",
        "title": "House Cleaning",
        "description": "I am looking for someone to clean my apartment before I move",
        "schedule": "Date: Tue, May 05 2020\nTime: 6:00 PM\nLength: 3.5 hours",
        "location": {
            "city": "San Francisco",
            "state": "CA",
            "zipCode": "94103"
        },
        "travelPreferences": "Professional must travel to my address"
    },
    "customer": {
        "customerID": "437282427635040257",
        "name": "John Doe"
    },
    "business": {
        "businessID": "437282430088732672",
        "name": "Mr. Clean's Sparkly Cleaning Service"
    }
}

test_message_dict = {
    "leadID": "299614694480093245",
    "customerID": "331138063184986319",
    "businessID": "286845156044809661",
    "message": {
        "messageID": "8699842694484326245",
        "createTimestamp": "1498760294",
        "text": "Do you offer fridge cleaning or is that extra?"
    }
}


class Test_TestThumbtack(unittest.TestCase):

    def test_create_test_data(self):
        return_dict = create_test_data()
        self.assertEqual(test_lead_dict, return_dict)

    def test_thumbtack_lead_json_to_list(self):
        data_list, column_list = thumbtack_lead_json_to_list(test_lead_dict)
        correct_data_list = ['437282430869512192', '1636428031', 'More information needed to give an estimate', '437282427823792129', 'House Cleaning', 'House Cleaning', 'I am looking for someone to clean my apartment before I move', 'Date: Tue, May 05 2020\nTime: 6:00 PM\nLength: 3.5 hours', 'San Francisco', 'CA', '94103', 'Professional must travel to my address', '437282427635040257', 'John Doe', '437282430088732672', "Mr. Clean's Sparkly Cleaning Service"]
        correct_column_list = ["thumbtack_lead_id", "contacted_time", "price", "thumbtack_request_id", "category", "title", "description", "schedule", "city", "state", "zip", "travel_preferences", "thumbtack_customer_id", "customer_name", "thumbtack_business_id", "thumbtack_business_name"]
        self.assertEqual(correct_data_list, data_list)
        self.assertEqual(correct_column_list, column_list)

    def test_thumbtack_message_json_to_list(self):
        data_list, column_list = thumbtack_message_json_to_list(test_message_dict)
        correct_data_list = ['299614694480093245', '331138063184986319', '286845156044809661', '8699842694484326245', '1498760294', 'Do you offer fridge cleaning or is that extra?']
        correct_column_list = ["thumbtack_lead_id", "thumbtack_customer_id", "thumbtack_business_id", "thumbtack_message_id", "contacted_time", "message_text"]
        self.assertEqual(correct_data_list, data_list)
        self.assertEqual(correct_column_list, column_list)

    def test_thumbtack_send_message(self):
        self.assertEqual(test_thumbtack_send_message("286845156044809661", "299614694480093245", "Hello John, how can I help you?"), 200)
        
