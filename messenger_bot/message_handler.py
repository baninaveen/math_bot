from messenger_bot.consts import *
from database.db_api import question_from_topic, options_and_answer
from messenger_bot.api_ai import APIAI
from messenger_bot.logger import log
from database.insert import insert_user_response
from messenger_bot.sender import send_text_message, send_question


def handle_message(message_text, sender_id, request_id):
    response = APIAI.Instance().message_response(
        message_text, sender_id)
    intent = response[RESULT][METADATA][INTENT_NAME]
    insert_user_response(request_id, str(response))
    log(response)
    if intent == STUDY:
        study_flow(sender_id, response, request_id)
    elif intent == GREETING:
        greeting_flow(sender_id, response)
    elif intent == DIAGNOSTIC_NO:
        diagnostic_no_flow(sender_id, response)
    elif intent == DIAGNOSTIC_YES:
        diagnostic_yes_flow(sender_id, response, request_id)
    elif intent == DEFAULT:
        send_text_message(sender_id,
                          response[RESULT][FULFILLMENT][SPEECH])
        send_helper_messages(sender_id)


def diagnostic_yes_flow(sender_id, response, request_id):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    question = question_from_topic('Arithmetic')
    options = options_and_answer(question[ID])
    send_question(sender_id, request_id, question, options,
                  remaining=3, topics=['Algebra', 'Geometry',
                                       'Word Problems', 'Statistics'],
                  diagnostic=True, test=True, topic='Arithmetic')


def diagnostic_no_flow(sender_id, response):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    send_helper_messages(sender_id)


def greeting_flow(sender_id, response):
    send_text_message(sender_id, 'Hi! How are you doing today? '
                                 'Here is what we can help you with:')
    send_helper_messages(sender_id)


def send_helper_messages(sender_id):
    send_text_message(sender_id, "You can Practice questions by typing "
                                 "something like "
                                 "'I want to do a question on Algebra'")
    send_text_message(sender_id, "If you have a question you want the solution "
                                 "you can type 'Solve: x^2 - 1 = 0'")


def study_flow(sender_id, response, request_id):
    send_text_message(sender_id, response[RESULT][FULFILLMENT][SPEECH])
    topic = response[RESULT][PARAMETERS][TOPICS]
    question = question_from_topic(topic)
    options = options_and_answer(question[ID])
    send_question(sender_id, request_id, question, options, topic=topic)