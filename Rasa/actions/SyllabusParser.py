from bs4 import BeautifulSoup, SoupStrainer
from pymongo import MongoClient
from datetime import datetime
import re
import requests
import logging

#TODO Retrieve credentials, and moodle token from credential manager
#TODO Retrieve mongo connection info from config file or environment variables
client = MongoClient(
          'mongo',
          27017,
          username='syllabuddy',
          password='syllabuddy123',
          authSource='syllabuddy',
          tls=True,
          tlsCAFile='/etc/ssl/rootCA.pem',
          tlsCertificateKeyFile='/etc/ssl/rasa-action.pem',
          tlsAllowInvalidCertificates=True,
)
db = client.syllabuddy
MOODLE_TOKEN = 'aac85c020d5bff5268d2ab04fc541bca'
MOODLE_WS_BASE_URL = ('https://syllabuddy.cmix.louisiana.edu/webservice/rest/server.php')
logger = logging.getLogger(__name__)
logging.basicConfig(level='DEBUG')


def updateSyllabus(courseID, content, date):
     rasaSoup = BeautifulSoup(content, 'html.parser')
     instructor = rasaSoup.find(string=re.compile("Instructor"))
     pre_reqs = rasaSoup.find(string=re.compile("Prerequisites")).find_next("div").string
     book_block = rasaSoup.find(string=re.compile("Textbook")).find_next("div")
     book = book_block.get_text()
     book += f'\n\n {book_block.find_next_sibling().get_text()}'
     email = rasaSoup.find(string=re.compile("Email")).parent.parent.get_text()
     office = rasaSoup.find(string=re.compile("Office:"))
     office += rasaSoup.find(string=re.compile("Office:")).next
     phone = rasaSoup.find(string=re.compile("Phone"))
     phone += rasaSoup.find(string=re.compile("Phone")).next
     syllabus_doc = { 'courseID': courseID,
         'instructor': instructor,
         'pre_reqs': pre_reqs,
         'book': book,
         'email': email,
         'office': office,
         'phone': phone,
         'timemodified': date}
     db.syllabuddy.update({"courseID": courseID}, syllabus_doc, True)


# Function to remove punctuation from a given input and return the processed string
def remove_punc(aString):
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

    for ele in aString:
        if ele in punc:
            aString = aString.replace(ele, "")
    return aString


#TODO rename courseID to shortname
def find_instructor(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['instructor']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['instructor']


def find_prerequisites(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['pre_reqs']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['pre_reqs']


def find_textbook(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['book']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['book']


def find_email(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['email']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['email']


def find_office(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['office']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['office']


def find_phone(courseID, moodleID):
    response = requests.get(
            f'{MOODLE_WS_BASE_URL}?wstoken={MOODLE_TOKEN}&'\
            f'moodlewsrestformat=json&'\
            f'wsfunction=mod_page_get_pages_by_courses&courseids[0]={moodleID}',
            verify=False)
    for page in response.json()['pages']:
        if 'syllabus' in page['name'].lower():
            date_obj = datetime.fromtimestamp(page['timemodified'])
            date_fmt = date_obj.strftime("%m/%d/%Y, %H:%M:%S")
            query_result = db.syllabuddy.find_one({'courseID': courseID})
            if not query_result:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            elif query_result['timemodified'] != date_fmt:
                updateSyllabus(courseID, page['content'], date_fmt)
                break
            else:
                return query_result['phone']

    query_result = db.syllabuddy.find_one({'courseID': courseID})
    return query_result['phone']



#####################################################################
# TESTS
######################################################################
def test_find_prerequisites(course):
    with open("/app/actions/Syllabi/" + course + ".html", encoding='utf8') as syllabus:
        rasaSoup = BeautifulSoup(syllabus, 'html.parser')

    if rasaSoup.find(string=re.compile("Prerequisites")) is None:
        return "No instructor found"
    else:
        result = rasaSoup.find(string=re.compile("Prerequisites")).find_next("p").string
        return result


# print(test_find_prerequisites("HCA540"))


def test_find_textbook(course):
    with open("/app/actions/Syllabi/" + course + ".html", encoding='utf8') as syllabus:
        rasaSoup = BeautifulSoup(syllabus, 'html.parser', parse_only=SoupStrainer(id="4"))

    if rasaSoup.find(string=re.compile("Textbook")).find_next("h4").find_next("a") is None:
        return "No textbooks found."
    else:
        result = rasaSoup.find(string=re.compile("Textbook")).find_next("h4").find_next("a").get_text(" ")
    return result


# print(test_find_textbook("chem123"))
# print(test_find_textbook("hca540"))
# print(test_find_textbook("MoodlePageChem123"))
# print(test_find_textbook("TEMP"))


def test_find_email(course):
    with open("/app/actions/Syllabi/" + course + ".html", encoding='utf8') as syllabus:
        rasaSoup = BeautifulSoup(syllabus, 'html.parser', parse_only=SoupStrainer(id="1"))

    if rasaSoup.find(string=re.compile("Email")) is None:
        return "No email address found"
    else:
        result = rasaSoup.find(string=re.compile("Email")).find_next("a").string
    return result


# print(test_find_email("chem123"))
# print(test_find_email("hca540"))
# print(test_find_email("MoodlePageChem123"))
# print(test_find_email("TEMP"))


def test_find_office(course):
    with open("/app/actions/Syllabi/" + course + ".html", encoding='utf8') as syllabus:
        rasaSoup = BeautifulSoup(syllabus, 'html.parser', parse_only=SoupStrainer(id="1"))

    if rasaSoup.find(string=re.compile("Office")) is None:
        return "No office found."
    else:
        result = rasaSoup.find(string=re.compile("Office:"))
        result += rasaSoup.find(string=re.compile("Office:")).next
    return result


# print(test_find_office("chem123"))
# print(test_find_office("hca540"))
# print(test_find_office("MoodlePageChem123"))
# print(test_find_office("TEMP"))


def test_find_phone(course):
    with open("/app/actions/Syllabi/" + course + ".html", encoding='utf8') as syllabus:
        rasaSoup = BeautifulSoup(syllabus, 'html.parser', parse_only=SoupStrainer(id="1"))

    if rasaSoup.find(string=re.compile("Phone")) is None:
        return "No phone number found."
    else:
        result = rasaSoup.find(string=re.compile("Phone"))
        result += rasaSoup.find(string=re.compile("Phone")).next
    return result

# print(test_find_phone("chem123"))
# print(test_find_phone("hca540"))
# print(test_find_phone("MoodlePageChem123"))
# print(test_find_phone("TEMP"))
