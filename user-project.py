from random import *
import json

edge_users = {}
project_users = {}
user_projects = {}

location_names = ['edge1', 'edge3', 'edge4']

location_proximity = {
                      'edge1': {'close':['edge3'], 'far':['edge4']}
                     ,'edge3': {'close':['edge1'], 'far':['edge4']}
                     ,'edge4': {'close':[], 'far':['edge1','edge3']}
                    }

def main():
    nr_users = 10
    nr_projects = 10
    nr_locations = len(location_names)

    user_names = ['locust%s' % (i+1) for i in range(nr_users)]
    user_names_copy = ['locust%s' % (i+1) for i in range(nr_users)]
    project_names = ['project%s' % (i + 1) for i in range(nr_projects)]

    # assigning users to locations
    user_locations_nr={}
    nr_users_copy = nr_users

    while(nr_users_copy > 0):
        for i in range(nr_locations):
            ln = location_names[i]
            if ln not in user_locations_nr:
                edge_users[ln] = []
                user_locations_nr[ln] = 0
            nr_users_copy -= 1
            user_locations_nr[ln] += 1
            # user_locations[ln].append(user_names_copy.pop(0))
            if nr_users_copy == 0:
                break

    for loc, count in user_locations_nr.items():
        for i in range(count):
            edge_users[loc].append(user_names_copy.pop(0))

    # assigning the first user to the porjects
    for i in range(nr_projects):
        pn = project_names[i]
        if pn not in project_users:
            project_users[pn] = []
        project_users[pn].append(user_names[i])

    # assigning a second or third user to the project
    for i in range(nr_projects):
        r = random()
        pn = project_names[i]
        if r <= 0.25:
            print('only one user for %s' % pn)
            continue
        if r > 0.25 and r <= 0.75:
            print('two users for %s' % pn)
            l = get_location_from_user(project_users[pn][0])
            u = get_user(l, pn)
            if u:
                project_users[pn].append(u)

        if r > 0.75:
            print('three users for %s' % pn)
            for i in range(2):
                l = get_location_from_user(project_users[pn][0])
                u = get_user(l, pn)
                if u:
                    project_users[pn].append(u)

    calculate_user_projects(user_names)

    # print(edge_users)
    # print(project_users)
    # print(user_projects)

    print(json.dumps(edge_users))
    print(json.dumps(project_users))
    print(json.dumps(user_projects))

def get_user(location, project):
    r = random()
    proximity = ''
    if r <= 0.5: # get user from the same location
        proximity = 'same'
    if r > 0.5 and r <= 0.85:
        proximity = 'close'
    if r > 0.85:
        proximity = 'far'
    return get_user_from_location(location, project, proximity)

def get_user_from_location(location, project, proximity):
    users = project_users[project]
    if proximity == 'same':
        for u in edge_users[location]:
            if u not in users:
                return u
        proximity = 'close'

    if proximity == 'close':
        count_close = len(location_proximity[location][proximity])
        if  count_close > 0:
            close_edge = location_proximity[location][proximity][randint(0, count_close-1)]
            for u in edge_users[close_edge]:
                if u not in users:
                    return u
        proximity = 'far'

    if proximity == 'far':
        count_far = len(location_proximity[location][proximity])
        if count_far> 0:
            far_edge = location_proximity[location][proximity][randint(0, count_far-1)]
            for u in edge_users[far_edge]:
                if u not in users:
                    return u
    return None

def get_location_from_user(user):
    for key, value in edge_users.items():
        for i in range(len(value)):
            v = value[i]
            if v == user:
                return key
    return None


def calculate_user_projects(user_names):
    for n in user_names:
        user_projects[n] = []

    for project, users in project_users.items():
        for user in users:
            for u in user_names:
                if user == u:
                    user_projects[user].append(project)

    #
    # print(user_locations)
    # print(user_projects)

if __name__ == "__main__":
    main()