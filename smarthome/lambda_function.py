# -*- coding: utf-8 -*-

import json
import urllib.request, urllib.error
from uuid import uuid4
import time
import random

AMAZON_API_USER_PROFILE = "https://api.amazon.com/user/profile"
AMAZON_OAUTH_HEADER = "x-amz-access-token"

# ユニークなUUIDを生成
def unique_id():
    return str(uuid4())

# APIの日付形式に合わせたGMTを返す
def utc_timestamp():
    return time.strftime("%Y-%m-%dT%H:%M:%S.00Z", time.gmtime())

def lambda_handler(event, context):
    print(json.dumps(event))
    header = event["directive"]["header"]

    if header["namespace"] == "Alexa.Discovery":
        return alexa_discover(header, event["directive"]["payload"])
    elif header["namespace"] == "Alexa.PowerController":
        return power_control(header, event["directive"]["endpoint"])
    elif header["namespace"] == "Alexa" and header["name"] == "ReportState":
        return report_status(header, event["directive"]["endpoint"])

    # 例外パターンはサンプルに含めてません
    print('un supported request')
    return None

# サンプルとしてランダムにステータスを返すだけ
def report_status(header, endpoint):
    status = random.choice(["ON", "OFF"])

    return power_control_response(header, endpoint, status)

def alexa_discover(header, payload):

    if header["name"] == "Discover":
        return discover_device(header, payload)

def discover_device(header, payload):

    # トークンを元にデバイスクラウドからユーザーに紐付いているデバイスを取得する
    endpoints = user_devices(payload)

    return build_discover_response(header, endpoints)

def user_devices(payload):

    # リクエストに含まれているトークンを元にamazonアカウントのプロフィールを取得
    user_profile = describe_user_profile(payload["scope"]["token"])
    print(user_profile)

    endpoint = {
        "endpointId": "appliance-001",
        "manufacturerName": "my smart home manufacturer",
        "friendlyName": "リビングの照明",
        "description": "明るさが調整できる照明です",
        "displayCategories": [
            "LIGHT"
        ],
        "cookie": {
            "extraDetail1": "スキルが使用するデバイスについての追加情報を表す、文字列名/値のペアです",
            "extraDetail2": "このプロパティの内容は5,000バイト以内でなければなりません",
            "extraDetail3": "APIはこのデータを使用せず、また解釈もしません"
        },
        "capabilities": [
            {
                "type": "AlexaInterface",
                "interface": "Alexa.PowerController",
                "version": "3",
                "properties": {
                    "supported": [
                    {
                        "name": "powerState"
                    }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                }
            },
            {
                "type": "AlexaInterface",
                "interface": "Alexa.BrightnessController",
                "version": "3",
                "properties": {
                    "supported": [
                    {
                        "name": "brightness"
                    }
                    ],
                    "proactivelyReported": False,
                    "retrievable": True
                }
            }            
        ]
    }
    return endpoint

def build_discover_response(header, endpoints):
    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": unique_id()
            },
            "payload": {
                "endpoints": [endpoints]
            }
        }
    }

    print(json.dumps(response))
    return response

def power_control(header, endpoint):
    print('power_control')

    # リクエストに含まれているトークンを元にamazonアカウントのプロフィールを取得
    user_profile = describe_user_profile(endpoint["scope"]["token"])
    print(user_profile)

    #########################################
    # 本来はここでユーザーのデバイスに対して操作を行う
    #########################################

    print("{} endpointId: {}".format(header["name"], endpoint["endpointId"]))

    if header["name"] == "TurnOn":
        return power_control_response(header, endpoint, "ON")
    else:
        return power_control_response(header, endpoint, "OFF")

def power_control_response(header, endpoint, value):
    name = "Response"
    if header["namespace"] == "Alexa" and header["name"] == "ReportState":
        name = "StateReport"

    response = {
        "context": {
            "properties": [ {
            "namespace": "Alexa.PowerController",
            "name": "powerState",
            "value": value,
            "timeOfSample": utc_timestamp(),
            "uncertaintyInMilliseconds": 500
            } ]
        },
        "event": {
            "header": {
            "namespace": "Alexa",
            "name": name,
            "payloadVersion": "3",
            "messageId": header["messageId"],
            "correlationToken": header["correlationToken"]
            },
            "endpoint": {
                "scope": {
                    "type": "BearerToken",
                    "token": endpoint["scope"]["token"]
                },
                "endpointId": endpoint["endpointId"]
            },
            "payload": {}
        }
    }

    print(json.dumps(response))
    return response

# LWAで取得したトークンを元にユーザーのプロフィールを取得
def describe_user_profile(access_token):

    req = urllib.request.Request(AMAZON_API_USER_PROFILE)
    req.add_header(AMAZON_OAUTH_HEADER, access_token)
    response = urllib.request.urlopen(req)
    if response.getcode() == 200:
        return json.loads(response.read())
    else:
        print(response.getcode())
        raise Exception(response.msg)
