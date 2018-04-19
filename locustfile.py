import json
import os
import re
import sys
import uuid

import time
from threading import Thread, Lock
import signal
from datetime import datetime
import random
from fractions import Fraction

from gevent.queue import Queue, Full, Empty
# from influxdb import InfluxDBClient
import gevent
from locust.core import TaskSet
from locust import HttpLocust, TaskSet, task, events, runners, stats
from locust.exception import StopLocust
import requests
# import statsd
import pandas as pd
import numpy as np

from loadgenerator import project, csrf, randomwords
# import metrics
import logparser



# host = os.environ.get("LOCUST_STATSD_HOST", "localhost")
# port = os.environ.get("LOCUST_STATSD_PORT", "8125")
# STATSD = statsd.StatsClient(host, port, prefix='loadgenerator')
METRICS_EXPORT_PATH     = os.environ.get("LOCUST_METRICS_EXPORT", "measurements")
MEASUREMENT_NAME        = os.environ.get("LOCUST_MEASUREMENT_NAME", "measurement")
MEASUREMENT_DESCRIPTION = os.environ.get("LOCUST_MEASUREMENT_DESCRIPTION", "linear increase")
DURATION                = int(os.environ.get("LOCUST_DURATION", "20"))
USERS                   = int(os.environ.get("LOCUST_USERS", '10'))
HATCH_RATE              = float(os.environ.get("LOCUST_HATCH_RATE", "1"))
LOAD_TYPE               = os.environ.get("LOCUST_LOAD_TYPE", "constant") # linear, constant, random, nasa, worldcup
SPAWN_WAIT_MEAN         = int(os.environ.get("LOCUST_SPAWN_WAIT_MEAN", "10"))
SPAWN_WAIT_STD          = int(os.environ.get("LOCUST_SPAWN_WAIT_STD", "4"))
USER_MEAN               = int(os.environ.get("LOCUST_USER_MEAN", "20"))
USER_STD                = int(os.environ.get("LOCUST_USER_STD", "5"))
WAIT_MEAN               = int(os.environ.get("LOCUST_WAIT_MEAN", "10"))
WAIT_STD                = int(os.environ.get("LOCUST_WAIT_STD", "4"))
TIMESTAMP_START         = os.environ.get("LOCUST_TIMESTAMP_START", '1998-06-02 08:50:00')
TIMESTAMP_STOP          = os.environ.get("LOCUST_TIMESTAMP_STOP", '1998-06-02 09:50:00')
WEB_LOGS_PATH           = os.environ.get("LOCUST_LOG_PATH", "logs") # path to nasa/worldcup logs
NR_SHARELATEX_USERS     = int(os.environ.get("LOCUST_NR_SHARELATEX_USERS", "5"))
PREDEF_PROJECTS         = os.environ.get("PREDEF_PROJECTS", '{"5ab1062fc2365e043f69239f":"remote"}')

os.environ["LOCUST_MEASUREMENT_NAME"] = MEASUREMENT_NAME
os.environ["LOCUST_MEASUREMENT_DESCRIPTION"] = MEASUREMENT_DESCRIPTION

current_milli_time = lambda: int(round(time.time() * 1000))

class RequestStats():
    def __init__(self):
        events.request_success += self.requests_success
        events.request_failure += self.requests_failure
        events.locust_error    += self.locust_error
        self.stats = {'Total':[]}

    def requests_success(self, request_type="", name="", response_time=0, **kw):
        # STATSD.timing(request_type + "-" + name, response_time)
        # print("%s - %s: %s" % (request_type, name, response_time))
        if name not in self.stats:
            self.stats[name] = []
        self.stats[name].append(response_time)
        self.stats['Total'].append(response_time)
        # if len(self.stats[name]) > 20:
        #     save_stats('lesh')
        # self.stats[name].append({'rt':response_time})
        # STATSD.timing("requests_success", response_time)

    def requests_failure(self, request_type="", name="", response_time=0, exception=None, **kw):
        # STATSD.timing(request_type + "-" + name + "-error", response_time)
        # if not request_type.startswith("WebSocket"):
        print("%s - %s: %s" % (request_type, name, response_time))
        # STATSD.timing("requests_failure", response_time)

    def locust_error(self, locust_instance=None, exception=None, tb=None):
        # STATSD.incr(locust_instance.__class__.__name__ + "-" + exception.__class__.__name__)
        # STATSD.incr("requests_error")
        pass

rs = RequestStats()

# def wait(self):
#     gevent.sleep(random.normalvariate(WAIT_MEAN, WAIT_STD))
# TaskSet.wait = wait

def save_stats(filename):
    res = {}
    for key, value in rs.stats.iteritems():
        value.sort()
        res[key]=[0]
        for i in range(1,11,1):
            fi = i*0.1
            inx = int(fi*len(value))
            if inx >= len(value):
                inx = len(value)-1
            res[key].append(value[inx])
    str_res = 'Percentage '
    skeys = sorted(res.keys())
    for i in range(0,12,1):
        for key in skeys:
            value = res[key]
            if i == 0:
                str_res += '%s ' % key.replace('_','\_')
            else:
                str_res += '%s ' % value[i-1]
        str_res += '\n'
        if i != 11:
            str_res += '%s ' % (0.1*i)
    # print str_res
    open('out/%s'% filename, 'w').write(str_res)
    pass

def save_csv(filename):
    cvs = stats.distribution_csv()
    old_rows = cvs.split('\n')
    new_columns = []
    nr_rows = 0
    nr_req_col = []
    method_names = []
    for old_row in old_rows:
        old_row = old_row.replace('"', '').replace('%','').replace('# ','')
        new_column = old_row.split(',')
        nr_req_col.append(new_column[1])
        nr_rows = len(new_column)
        new_column[0] = new_column[0].replace("_","\_").split(' ')
        new_column[0] = new_column[0][1] if len(new_column[0]) > 1 else new_column[0][0]
        method_names.append(new_column[0])
        new_columns.append(new_column)

        # name = words[0].strip('"').split(' ')
        # name = name[1] if len(name) > 1 else name[0]
        # nr_req =
    k = 0
    dist_res = ''
    for i in range(0, nr_rows):
        if i == 1:
            continue
        new_row = []
        for j in range(0, len(new_columns)):
            new_row.append(new_columns[j][i])
        new_row_str = ' '.join(new_row)
        dist_res += "%s\n" % new_row_str

    req_res = ''
    for i in range(0, len(method_names)):
        req_res += "%s %s\n" % (method_names[i], nr_req_col[i])

    open('out/%s(%s)'% (filename,'dist'), 'w').write(dist_res)
    open('out/%s(%s)'% (filename,'req'), 'w').write(req_res)

def login(l):
    resp = l.client.get("/login", name='get_login_page')
    l.csrf_token = csrf.find_in_page(resp.content)

    data = {
        "_csrf": l.csrf_token,
        "email": l.email,
        "password": "locust"
    }
    tb= current_milli_time()
    r = l.client.post("/login", data, name='login')
    ta= current_milli_time()
    # print ('%s' % str(ta-tb))
    assert r.json().get("redir", None) == "/project"


def settings(l):
    l.client.get("/user/settings", name='get_settings')
    d = dict(_csrf=l.csrf_token, email=l.email, first_name=l.email.split('@')[0].title(), last_name="Swarm")
    assert l.client.post("/user/settings", json=d, name="update_settings").text == "OK"


def create_tag(l):
    name = randomwords.sample(1, 1)[0]
    data = {"_csrf": l.csrf_token, "name": name}
    r = l.client.post("/tag", data, name='create_tag')
    if r.status_code != 200:
        print 'user %s tried to create tag %s' % (l.email, name)
    pass


def logout(l):
    resp = l.client.get("/logout", name='logout')
    l.interrupt(reschedule=True)


logins_per_acc = 2
user = 1#1
mutex = Lock()

class ProjectOverview(TaskSet):
    # tasks = { project.Page: 100, create_tag: 10, settings: 5, logout: 20}
    tasks = { project.Page: 100, logout: 20}

    def on_start(self):
        global user
        global logins_per_acc
        mutex.acquire()
        i = NR_SHARELATEX_USERS if (int(user) % NR_SHARELATEX_USERS) == 0 else (int(user) % NR_SHARELATEX_USERS)
        # print "## %d %d" % (user, i)

        self.email = "locust%d@sharelatex.dev" % i
        user += Fraction(1, logins_per_acc)
        print('Using user: %s' % self.email)
        mutex.release()

        login(self)

        r = self.client.get("/project", name='get_project_list')
        self.csrf_token = csrf.find_in_page(r.content)
        self.predef_projects = json.loads(PREDEF_PROJECTS)
        self.nr_users = NR_SHARELATEX_USERS

        # assert len(self.projects) > 0, "No project found, create some!"

class UserBehavior(TaskSet):
    tasks = {ProjectOverview: 1}
    # def on_start(self):

class WebsiteUser(HttpLocust):
    if LOAD_TYPE == "nasa" or LOAD_TYPE == "worldcup":
        def __init__(self, client_id, timestamps, queue):
            self.request_timestamps = timestamps
            self.request_number = 1
            self.client_id = client_id
            self.client_queue = queue
            super(WebsiteUser, self).__init__()

    # host = 'http://192.168.56.1:8080'
    host = 'http://localhost:8080'
    task_set = UserBehavior
    min_wait = 2000
    max_wait = 4000



def stop_measure(started_at):
    ended_at = datetime.utcnow()
    metadata = {}
    for k, v in os.environ.items():
        if k.startswith("LOCUST_"):
            name = k[len("LOCUST_"):]
            metadata[name.lower()] = v
    # compatibility
    metadata['name']        = metadata['measurement_name']
    metadata['description'] = metadata['measurement_description']
    # metrics.export(metadata, started_at, ended_at)

    save_stats('%s-%s'% (metadata['name'],str(uuid.uuid4())[:4]))
    # open('out/%s-%s'% (metadata['name'],ended_at), 'w').write(cvs)

    os.kill(os.getpid(), signal.SIGINT)

def constant_measure(*args, **kw):
    # wait for the load generator to take effect
    time.sleep(10)
    started_at = datetime.utcnow()
    time.sleep(DURATION)
    stop_measure(started_at)

def start_hatch(users, hatch_rate):
    payload = dict(locust_count=users, hatch_rate=hatch_rate)
    r = requests.post("http://localhost:8089/swarm", data=payload)
    print(r.text)

def print_color(text):
    print("\x1B[31;40m%s\x1B[0m" % text)

def process_requests(self):
    i = self.locust.request_number
    timestamps = self.locust.request_timestamps
    if i < timestamps.size:
        delta = (timestamps.iloc[i] - timestamps.iloc[i - 1]) / np.timedelta64(1, 's')
        print("client %s waits or %s" % (self.locust.client_id, delta))
        gevent.sleep(delta)
        self.locust.request_number += 1
    else:
        try:
            idx, timestamps = self.locust.client_queue.get(timeout=1)
            self.client_id = idx
            self.request_timestamps = timestamps
            self.request_number = 1
        except Empty:
            raise StopLocust("stop this instance")

def report_users():
    while True:
        try:
            val = runners.locust_runner.user_count
            # STATSD.set("website_users", val)
        except SystemError as e:
            print("could not update `website_users` statsd counter: %s" % e)
        gevent.sleep(2)

GREENLETS = []
def replay_log_measure(df):
    TaskSet.wait = process_requests
    runner = runners.locust_runner
    locust = runner.locust_classes[0]
    start_hatch(0, 1)

    by_session = df.groupby(["started_at", "client_id", "session_id"])
    started_at = by_session.first().timestamp.iloc[0]
    real_started_at = datetime.utcnow()

    real_started_at = datetime.utcnow()
    queue = Queue(maxsize=1)
    runner.locusts.spawn(report_users)

    for idx, client in by_session:
        timestamps = client.timestamp
        now = timestamps.iloc[0]
        gevent.sleep((now - started_at) / np.timedelta64(1, 's'))
        print("sleep (%s - %s) %s" % (now, started_at, (now - started_at) / np.timedelta64(1, 's')))
        started_at = now
        def start_locust(_):
            try:
                l = WebsiteUser(idx[1], timestamps, queue)
                l.run()
            except gevent.GreenletExit:
                pass
        try:
            queue.put((idx[1], timestamps), block=False)
        except Full:
            runner.locusts.spawn(start_locust, locust)
    stop_measure(real_started_at)

def random_measure():
    runner = runners.locust_runner
    locust = runner.locust_classes[0]
    def start_locust(_):
        try:
            locust().run()
        except gevent.GreenletExit:
            pass

    print_color("start hatching with %d/%d" % (USER_MEAN, len(runner.locusts)))
    start_hatch(0, 1)
    while USER_MEAN > len(runner.locusts):
        runner.locusts.spawn(start_locust, locust)
        time.sleep(2)

    started_at = datetime.utcnow()

    while True:
        seconds = (datetime.utcnow() - started_at).seconds
        if seconds > DURATION:
            break
        print("%d seconds left!" % (DURATION - seconds))
        new_user = -1
        while new_user < 0:
            new_user = int(random.normalvariate(USER_MEAN, USER_STD))

        print_color("new user %d clients" % new_user)
        if new_user > len(runner.locusts):
            while new_user > len(runner.locusts):
                runner.locusts.spawn(start_locust, locust)
                print("spawn user: now: %d" % len(runner.locusts))
                time.sleep(1)
        elif new_user < len(runner.locusts):
            locusts = list([l for l in runner.locusts])
            diff = len(locusts) - new_user
            if diff > 0:
                for l in random.sample(locusts, diff):
                    if new_user >= len(runner.locusts): break
                    try:
                        runner.locusts.killone(l)
                    except Exception as e:
                        print("failed to kill locust: %s" % e)
                    print("stop user: now: %d" % len(runner.locusts))
        # STATSD.gauge("user", len(runner.locusts))
        wait = random.normalvariate(SPAWN_WAIT_MEAN, SPAWN_WAIT_STD)
        print_color("cooldown for %f" % wait)
        time.sleep(wait)
    stop_measure(started_at)

def read_log(type):
    if type == "nasa":
        read_log = logparser.read_nasa
    else: # "worldcup"
        read_log = logparser.read_worldcup
    df = read_log(WEB_LOGS_PATH)
    df = df[(df.timestamp > pd.Timestamp(TIMESTAMP_START)) & (df.timestamp < pd.Timestamp(TIMESTAMP_STOP))]
    filter = df["type"].isin(["HTML", "DYNAMIC", "DIRECTORY"])
    if type == "worldcup":
        #filter = filter & df.region.isin(["Paris", "SantaClara"])
        filter = filter & df.region.isin(["Paris"])
    return df[filter]

def session_number(v):
    diff = v.timestamp.diff(1)
    diff.fillna(0, inplace=True)
    sessions = (diff > pd.Timedelta(minutes=10)).cumsum()
    data = dict(client_id=v.client_id, timestamp=v.timestamp,
                session_id=sessions.values)
    return pd.DataFrame(data)

def started_at(v):
    data = dict(client_id=v.client_id, timestamp=v.timestamp, session_id=v.session_id,
                started_at=[v.timestamp.iloc[0]] * len(v.timestamp))
    return pd.DataFrame(data)

def group_log_by_sessions(df):
    df = df.sort_values("timestamp")
    per_client = df.groupby(df.client_id, sort=False)
    with_session = per_client.apply(session_number)
    by = [with_session.client_id, with_session.session_id]
    return with_session.groupby(by).apply(started_at)

def measure():
    # RequestStats()
    time.sleep(5)
    print "load type: %s" % LOAD_TYPE
    if LOAD_TYPE == "constant":
        start_hatch(USERS, HATCH_RATE)
        events.hatch_complete += constant_measure
    elif LOAD_TYPE == "linear":
        start_hatch(USERS, HATCH_RATE)
        started_at = datetime.utcnow()
        def linear_measure(*args, **kw):
            stop_measure(started_at)
        events.hatch_complete += linear_measure
    elif LOAD_TYPE == "random":
        random_measure()
    elif LOAD_TYPE == "nasa" or LOAD_TYPE == "worldcup":
        df = read_log(LOAD_TYPE)
        replay_log_measure(group_log_by_sessions(df))
    else:
        sys.stderr.write("unsupported load type: %s" % LOAD_TYPE)
        sys.exit(1)

is_debug = os.environ.get("PYCHARM", "0") == '1'
if is_debug:
    x = WebsiteUser()
    x.run()
else:
    Thread(target=measure).start()


# if __name__ == '__main__':
