# -*- coding: utf-8 -*-
import os
import json

def lambda_handler(event, context):
    print(json.dumps(event))

    if event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event["session"])
    elif event['request']['type'] == "SessionEndedRequest":
        return return_cancel()

    return on_launch()

def on_launch():
    print("on_launch")
    data = {
        "title": "ご主人様、こんにちわ。",
        "speech": "こんにちわ、ご主人様。「ただいま」と話しかけてみて下さい。",
        "reprompt": "「ただいま」と話しかけてみて下さい。",
        "close_session": False,
        "session_attribute": None
    }
    return build_speechlet_response(data)

def on_intent(request, session):
    intent_name = request['intent']['name']
    print("intent name: {}".format(intent_name))

    if intent_name == "ImHomeIntent":
        return return_question()
    elif intent_name == "HungryIntent":
        if not is_action_phase(session, "CHOSE_ACTION"):
            return return_question()        
        return return_eat(request, session)
    elif intent_name == "MealIntent":
        if not is_action_phase(session, "SELECT_MEAL"):
            return return_question()        
        return return_meal(request, session)
    elif intent_name == "BathIntent":
        if not is_action_phase(session, "CHOSE_ACTION"):
            return return_question()        
        return return_bath(request, session)
    elif intent_name == "AMAZON.HelpIntent":
        return return_help()
    else:
        return return_help()

def return_help():
    data = {
        "title": "執事との接し方。",
        "speech": "こんにちわ、ご主人様。私はご主人様に使える執事です。身の回りのお世話はおまかせ下さい。",
        "reprompt": None,
        "close_session": True,
        "session_attribute": None
    }
    return build_speechlet_response(data)

def return_question():
    data = {
        "title": "おかえりなさいませ、ご主人様。",
        "speech": "おかえりなさいませ、ご主人様。お食事にしますか？ それとも、お風呂にしますか？",
        "reprompt": "お食事にしますか、お風呂にしますか？",
        "close_session": False,
        "session_attribute": {"action": "CHOSE_ACTION"}
    }

    return build_speechlet_response(data)

def return_bath(request, session):
    data = {
        "title": "お風呂ですね。",
        "speech": "お風呂ですね。すぐ用意しますので、くつろいでおまちになってくださいね。",
        "reprompt": None,
        "close_session": True,
        "session_attribute": None
    }

    return build_speechlet_response(data)

def return_eat(request, session):
    data = {
        "title": "お食事ですね。",
        "speech": "お食事ですね。今日はどんな料理が食べたいですか？",
        "reprompt": "今日はどんな料理が食べたいですか？",
        "close_session": False,
        "session_attribute": {"action": "SELECT_MEAL"}
    }

    return build_speechlet_response(data)

def return_meal(request, session):
    meal_name = request["intent"]["slots"]["meal_name"]
    data = {
        "title": "{}ですね。".format(meal_name["value"]),
        "speech": "{}ですね。すぐに用意しますので、少しお待ち下さい。".format(meal_name["value"]),
        "reprompt": None,
        "close_session": True,
        "session_attribute": None
    }

    return build_speechlet_response(data)

def return_cancel():
    data = {
        "title": "さようなら",
        "speech": "いつでも執事にお申し付け下さいね。",
        "reprompt": None,
        "close_session": True,
        "session_attribute": None
    }

    return build_speechlet_response(data)

def build_speechlet_response(data):

    return_message = {
        "outputSpeech": {
            "type": "PlainText",
            "text": data["speech"]
        },
        "card": {
            "type": "Simple",
            "title": data["title"],
            "content": data["speech"]
        },
        "shouldEndSession": data["close_session"]
    }
    if data["reprompt"] is not None:
        return_message["reprompt"] = {
            "outputSpeech": {
                "type": "PlainText",
                "text": data["reprompt"]
            }            
        }

    return build_response(return_message, data["session_attribute"])

def build_response(speechlet_response, session_attribute):
    response = {
        'version': '1.0',
        'response': speechlet_response
    }
    if session_attribute:
        response["sessionAttributes"] = session_attribute

    print(json.dumps(response))
    return response

def is_action_phase(session, phase):
    if session["new"]:
        print("session is new")
        return False

    if "attributes" not in session or "action" not in session["attributes"]:
        print("action attribute not found in session")
        return False

    return session["attributes"]["action"] == phase
