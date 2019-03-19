import os
import requests
import datetime
import json
import numpy as np
import traceback

def main():
    apiKey = getTodoistKey()
    tasks = getAllActiveTasks(apiKey)
    parsed = parseTasks(tasks)

def getTodoistKey():
    with open('todoist.key') as keyFile:
        key = keyFile.readline()
    return key

def getProjects(key):
    response = requests.get("https://beta.todoist.com/API/v8/projects", headers={"Authorization": "Bearer %s" % key}).json()
    return response

def getAllActiveTasks(key):
    # get all projects
    tasks = []
    projects  = getProjects(key)
    for project in projects:
        projectID = project['id']
        _tasks = requests.get("https://beta.todoist.com/API/v8/tasks", 
            params={"project_id":projectID},
            headers={"Authorization": "Bearer %s" % key}
            ).json()
        tasks = tasks + _tasks

    return tasks

def parseTasks(tasks):
    parsedTasks = [None,None,None,None,None]
    for task in tasks:
        try:
            taskClass = Task()
            if 'datetime' in task['due']:
                dueTime = task['due']['datetime']
                strpdTime = datetime.datetime.strptime(dueTime[:-1], '%Y-%m-%dT%H:%M:%S')
                taskClass.dateTimeString = strpdTime.strftime('%a %m/%d %I:%M %p')
                taskClass.content = task['content']
                parsedTasks = [taskClass] + parsedTasks
            elif 'date' in task['due']:
                dueDate = task['due']['date']
                strpdTime = datetime.datetime.strptime(dueDate, '%Y-%m-%d')
                taskClass.dateTimeString = strpdTime.strftime('%a %m/%d %I:%M %p')
                taskClass.content = task['content']
                parsedTasks = [taskClass] + parsedTasks
            else:
                print("ignored a task")
        except Exception as exc:
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print("error parsing a task")
        
    return parsedTasks

class Task():
    dateTimeString = ""
    content = ""


if __name__ == "__main__":
    main()