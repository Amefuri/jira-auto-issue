from atlassian import Jira
import csv
import sys

jiraBaseUrl = '[baseUrl]'
projectCode = '[projectCode]'
username = '[username]'
apiToken = '[apiToken]'
csvFileName = '[csvFile.csv]'
iosLabel = 'iOS'
androidLabel = 'Android'

def safe_index(list: list, index: int):
    if len(list) > index:
        return list[index]
    else:
        return ''

def create_issue(summary: str, description: str, label: str):
    return jira.issue_create(fields={
        'project': {'key': projectCode},
        'issuetype': {
            "name": "Story"
        },
        'summary': summary,
        'description': description,
        "labels": [label]
    })

def link_issue(outwardIssueId: str, inwardIssueId: str):
    return jira.create_issue_link({
        "outwardIssue": {
            "key": outwardIssueId
        },
        "inwardIssue": {
            "key": inwardIssueId
        },
        "type": {
            "name": "Cloners"
        }
    })

jira = Jira(
    url=jiraBaseUrl,
    username=username,
    password=apiToken)

with open(csvFileName, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        print('Summary = ', safe_index(row, 0),
              " Detail = ", safe_index(row, 1))

confirm = input('Confirm(y/n)?:')
if confirm.lower() != 'y':
    sys.exit(0)

with open(csvFileName, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        eachSummary = safe_index(row, 0)
        eachDescription = safe_index(row, 1)
        response = create_issue(eachSummary, eachDescription, iosLabel)
        outwardIssueId = response['key']
        response = create_issue(eachSummary, eachDescription, androidLabel)
        inwardIssueId = response['key']
        link_issue(outwardIssueId, inwardIssueId)

print("DONE")
