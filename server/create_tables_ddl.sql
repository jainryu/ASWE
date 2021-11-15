/*
Author : Animesh Bhasin
Description : DDL for talking potatoes
Version : 1
*/


------------------------------------------------------------
-- Create schemas
CREATE SCHEMA IF NOT EXISTS fb;
CREATE SCHEMA IF NOT EXISTS thumbtack;
CREATE SCHEMA IF NOT EXISTS talking_potato;


------------------------------------------------------------
-- Create users table to store user information
------------------------------------------------------------

CREATE TABLE talking_potato.users (
	user_id varchar NOT NULL,
	username varchar NULL,
	"password" varchar NULL,
	email varchar NULL,
	phone_number varchar NULL,
	thumbtack_user_id varchar NULL,
	facebook_user_id varchar NULL,
	thumbtack_password varchar NULL,
	thumbtack_api_key varchar NULL,
	fb_app_secret_key varchar NULL,
	fb_page_access_token varchar NULL,
	created_at timestamptz NULL DEFAULT CURRENT_TIMESTAMP,
	thumbtack_business_id varchar NULL
);



------------------------------------------------------------
-- Create messages table to store facebook messages
------------------------------------------------------------

CREATE TABLE fb.messages (
	sender_id varchar NULL,
	recipient_id varchar NULL,
	"timestamp" timestamp NULL,
	message_text varchar NULL,
	page_id varchar NULL,
	update_time timestamp NULL,
	created_at timestamptz NULL DEFAULT CURRENT_TIMESTAMP,
	message_id varchar
);
------------------------------------------------------------
-- Create messages table to store thumbtack messages
------------------------------------------------------------

CREATE TABLE thumbtack.messages (
	thumbtack_lead_id varchar NULL,
	thumbtack_customer_id varchar NULL,
	thumbtack_business_id varchar NULL,
	thumbtack_message_id varchar NULL,
	contacted_time timestamp NULL,
	message_text varchar NULL,
	created_at timestamptz NULL DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------------------
-- Create leads table to store thumbtack leads
------------------------------------------------------------
CREATE TABLE thumbtack.leads (
	thumbtack_lead_id varchar NULL,
	contacted_time timestamp NULL,
	price varchar NULL,
	thumbtack_request_id varchar NULL,
	category varchar NULL,
	title varchar NULL,
	description varchar NULL,
	schedule varchar NULL,
	city varchar NULL,
	state varchar NULL,
	zip varchar NULL,
	travel_preferences varchar NULL,
	thumbtack_customer_id varchar NULL,
	customer_name varchar NULL,
	thumbtack_business_id varchar NULL,
	thumbtack_business_name varchar NULL,
	created_at timestamptz NULL DEFAULT CURRENT_TIMESTAMP
);

------------------------------------------------------------
-- Create messages view to store aggregate message info
------------------------------------------------------------
create or replace
view talking_potato.messages as
select
	thumbtack_customer_id as sender_id,
	m.thumbtack_business_id as recipient_id,
	contacted_time ,
	message_text,
	thumbtack_message_id,
	'thumbtack' as user_source,
	u.user_id
from
	thumbtack.messages m
join talking_potato.users u on
	u.thumbtack_business_id = m.thumbtack_business_id
union
select
	sender_id,
	recipient_id ,
	"timestamp" as contacted_time,
	message_text ,
	message_id,
	'facebook',
	u.user_id
from
	fb.messages m2
join talking_potato.users u on
	u.facebook_user_id = m2.recipient_id ;
