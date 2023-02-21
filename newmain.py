from jira import JIRA
import csv
import sys
import json

jiraBaseUrl = ''
projectCode = 'JL' #'BEEB'  # input('Enter project code:')
username = ''
apiToken = ''
csvFileName = 'input.csv'  # input('Enter csv file name(ex. "input.csv"):')
iosLabel = 'iOS'
androidLabel = 'Android'
iosIssueType = 'iOS'
androidIssueType = 'Android'
apiLabel = 'API'
apiIssueType = 'Task'
designLabel = 'Design'
designIssueType = 'Task'
linkIssueType = 'Cloners'

def safe_index(list: list, index: int):
    if len(list) > index:
        return list[index]
    else:
        return ''

def create_issue(summary: str, description: str, label: str, issueType: str, storyPoints: float):
    return jira.create_issue(fields={
        'project': {'key': projectCode},
        'issuetype': {
            "name": issueType
        },
        'summary': summary,
        'description': description,
        'customfield_10016': storyPoints,
        "labels": [label]
    })

def link_issue(inwardIssue, outwardIssue):
    return jira.create_issue_link(linkIssueType, inwardIssue.key, outwardIssue.key)

jira = JIRA(server=jiraBaseUrl, basic_auth=(username, apiToken))

# issue = jira.issue('JL-1909')
# print(issue.key)
# print(issue.fields.project.key)            # 'JRA'
# print(issue.fields.project.id)
# print(issue.fields.issuetype.name)         # 'New Feature'
# print(issue.fields.reporter.displayName)   # 'Mike Cannon-Brookes [Atlassian]'

with open(csvFileName, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        print('Summary = ', safe_index(row, 0),
              " Detail = ", safe_index(row, 1),
              " Story Points = ", safe_index(row, 2))

confirm = input('Confirm(y/n)?:')
if confirm.lower() != 'y':
    sys.exit(0)

with open(csvFileName, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        eachSummary = safe_index(row, 0)
        eachDescription = safe_index(row, 1)
        eachStoryPoints = float(safe_index(row, 2))

        if eachSummary.find('[API]') != -1:
            response = create_issue(eachSummary, eachDescription, apiLabel, apiIssueType, eachStoryPoints)
        elif eachSummary.find('[Design]') != -1:
            response = create_issue(eachSummary, eachDescription, designLabel, designIssueType, eachStoryPoints)
        else:
            outwardIssue = create_issue(eachSummary, eachDescription, iosLabel, iosIssueType, eachStoryPoints)
            inwardIssue = create_issue(eachSummary, eachDescription, androidLabel, androidIssueType, eachStoryPoints)
            link_issue(inwardIssue, outwardIssue)

print("DONE")
