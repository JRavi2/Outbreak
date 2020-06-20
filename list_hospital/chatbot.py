import requests 
import json
from .Infermedica import *

answer_norm = {
    'yes': 'present',
    'y': 'present',
    'present': 'present',
    'no': 'absent',
    'n': 'absent',
    'absent': 'absent',
    '?': 'unknown',
    'skip': 'unknown',
    'unknown': 'unknown',
    'dont know': 'unknown',
    'sí': 'present',
    'si': 'present',
    'no lo sé': 'unknown',
    'no lo se': 'unknown',
    'omitir': 'unknown',
    'omita': 'unknown',
    'salta': 'unknown',
}

def diagnose(age,sex,evidence):
    url ="https://api.infermedica.com/v2/diagnosis"

    payload={'age':age,'sex':sex,'evidence':evidence,'extras':{
            # this is to avoid very improbable diagnoses at output and ensure there are no more than 8 results
            # recommended to use for virtually any app, this should become the default mode soon
            'enable_adaptive_ranking': True,
            # voice/chat apps usually can't handle group questions well
            'disable_groups': True
        }}
    # payload={'age': 18, 'sex': 'male', 'evidence': [{'id': 's_21', 'choice_id': 'present', 'initial': True}, {'id': 's_102', 'choice_id': 'present', 'initial': True}], 'extras': {'enable_adaptive_ranking': True, 'disable_groups': True}}
    header={'App-Id':'33e7b86d','App-Key':'1c80f2d4577c86270a5c69f560068804','Content-Type':'application/json'}
    r=requests.post(url,data=json.dumps(payload),headers=header)
    

    data=r.json()
    # print(data['question'])
    return data

def read_complaints(complaints, evidence, age, sex, auth_string, case_id, language_model=None):
    """Keep reading complaint-describing messages from user until empty message read (or just read the story if given).
    Will call the /parse endpoint and return mentions captured there."""
    context = []  # a list of ids of present symptoms in the order of reporting
    mentions = []
    for i in range(len(complaints)):
        portion = call_parse(complaints[i], auth_string, case_id, context, language_model=language_model).get(
            'mentions', [])
        if portion:
            mentions.extend(portion)
            # remember the mentions understood as context for next /parse calls
            context.extend([m['id'] for m in mentions if m['choice_id'] == 'present'])
    evidence.extend(mentions_to_evidence(mentions))
    question_item = diagnose(age, sex, evidence)['question']['text']
    return mentions, evidence, question_item

def conduct_interview(evidence, ans, age, sex, case_id, auth, language_model=None):
    """Keep asking questions until API tells us to stop or the user gives an empty answer."""
    resp = diagnose(age, sex, evidence)
    question_struct = resp['question']
    diagnosis = resp['conditions']
    should_stop_now = resp['should_stop']
    if should_stop_now:
        # triage recommendation must be obtained from a separate endpoint, call it now
        # and return all the information together
        # TRIAGE TO BE IMPLEMENTED IN THE FUTURE #
        # triage_resp = call_triage(evidence, age, sex, case_id, auth, language_model=language_model)
        return diagnosis, None, evidence
    if question_struct['type'] == 'single':
        question_items = question_struct['items']
        assert len(question_items) == 1  # this is a single question
        question_item = question_items[0]
        observation_value = answer_norm[ans]
        # render(request,'')
        if observation_value is not None:
            evidence.extend(question_answer_to_evidence(question_item, observation_value))
    return diagnosis, question_struct['text'], evidence

# evidence= [{'id': 's_21', 'choice_id': 'present', 'initial': True}, {'id': 's_102', 'choice_id': 'present', 'initial': True}, {'id': 's_1193', 'choice_id': 'absent', 'initial': False}]

# diagnose(18,"male",evidence)
