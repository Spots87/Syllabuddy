# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import actions.SyllabusParser
import logging

logging = logging.Logger(__name__)

def extract_metadata_from_tracker(tracker):
    events = tracker.current_state()['events']
    user_events = []
    for e in events:
        if e['event'] == 'user':
            user_events.append(e)

    return user_events[-1]['metadata']

class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Hello World!")

        return []


class ActionRetrieveInstructor(Action):

    def name(self) -> Text:
        return "action_retrieve_instructor"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_instructor(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []


class ActionRetrievePrerequisites(Action):

    def name(self) -> Text:
        return "action_retrieve_prerequisites"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_prerequisites(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []


class ActionRetrieveTextbook(Action):

    def name(self) -> Text:
        return "action_retrieve_textbook"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[
        Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_textbook(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []


class ActionRetrieveEmail(Action):

    def name(self) -> Text:
        return "action_retrieve_email"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_email(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []


class ActionRetrieveOffice(Action):

    def name(self) -> Text:
        return "action_retrieve_office"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_office(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []


class ActionRetrievePhone(Action):

    def name(self) -> Text:
        return "action_retrieve_phone"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        metadata=extract_metadata_from_tracker(tracker)
        courseID = metadata['courseID']
        moodleID = metadata['moodleID']
        response = actions.SyllabusParser.find_phone(courseID, moodleID)
        dispatcher.utter_message(text=response)

        return []
