from atlassian import Jira
import csv
import sys

jiraBaseUrl = ""
projectCode = 'JL' #'BEEB'  # input('Enter project code:')
username = ''  # input('Enter username:')
apiToken = ''  # input('Enter JIRA api token:')
csvFileName = 'input.csv'  # input('Enter csv file name(ex. "input.csv"):')
iosLabel = 'iOS'
androidLabel = 'Android'
iosIssueType = 'iOS'
androidIssueType = 'Android'
apiLabel = 'API'
apiIssueType = 'Task'
designLabel = 'Design'
designIssueType = 'Task'

def safe_index(list: list, index: int):
    if len(list) > index:
        return list[index]
    else:
        return ''

def create_issue(summary: str, description: str, label: str, issueType: str, storyPoints: float):
    return jira.issue_create(fields={
        'project': {'key': projectCode},
        'issuetype': {
            "name": issueType
        },
        'summary': summary,
        'description': description,
        # 'timetracking': {
        #     'originalEstimate': "{0}d".format(storyPoints)
        # },
        # 'customfield_10016': storyPoints,
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
        eachStoryPoints = safe_index(row, 2)

        if eachSummary.find('[API]') != -1:
            response = create_issue(eachSummary, eachDescription, apiLabel, apiIssueType, eachStoryPoints)
            response.update(fields={"customfield_10016": eachStoryPoints})
        elif eachSummary.find('[Design]') != -1:
            response = create_issue(eachSummary, eachDescription, designLabel, designIssueType, eachStoryPoints)
            response.update(fields={"customfield_10016": eachStoryPoints})
        else:
            response = create_issue(eachSummary, eachDescription, iosLabel, iosIssueType, eachStoryPoints)
            # issue = jira.issue(response['key'])
            # print(issue)
            # issue.update(fields={"customfield_10016": eachStoryPoints})
            outwardIssueId = response['key']
            response = create_issue(eachSummary, eachDescription, androidLabel, androidIssueType, eachStoryPoints)
            # issue = jira.issue(response['key'])
            # issue.update(fields={"customfield_10016": eachStoryPoints})
            inwardIssueId = response['key']
            link_issue(outwardIssueId, inwardIssueId)

print("DONE")
