# Talking Potatoes

###How to Test Our Service
- Download all modules included in server/requirements.txt
- BASE_URL = https://tp-leads-app.herokuapp.com
- You can access our service using the paths along with the requested params as described in the following API documentation

****

###API Documentation
**Registration** 
- POST {{BASE_URL}}/register
    - Query params: 
      - [required]  email(varchar)
      - [required] username(varchar)
      - [required] password(varchar)

**Message Analytics** <br/> - GET {{BASE_URL}}/message_analytics


****

###Third Party APIs
1. [Thumbtack](https://pro-api.thumbtack.com/docs/#introduction)
   1. misc/fb/thumbtack_conn.py : used to send messages to the leads

2. Facebook
