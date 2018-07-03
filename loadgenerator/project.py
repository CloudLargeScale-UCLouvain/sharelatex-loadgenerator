import socketio
import gevent
import random
import os
import re
import string
import uuid
import json
import time
import sys
from . import ROOT_PATH, csrf, randomwords
from gevent.exceptions import ConcurrentObjectUseError
from locust import TaskSet, task
from websocket import WebSocketConnectionClosedException
from locust.events import request_success


# from requests import Request, Session
current_milli_time = lambda: int(round(time.time() * 1000))
pos_triggered = pos_registered = 0 #delete this in the end

class Websocket():
    def __init__(self, page):
        self.c = socketio.Client(page.locust)
        self.l = page
        self.sent_doc_version = 0
        self.pending_text = None
        # self.c.on("clientTracking.clientUpdated", self.noop)
        self.c.on("clientTracking.clientUpdated", self.on_update_position)
        self.c.on("clientTracking.clientDisconnected", self.noop)
        self.c.on("new-chat-message", self.on_chat)
        self.c.on("reciveNewFile", self.noop)
        self.c.on("connectionAccepted", self.noop)
        self.c.on("otUpdateApplied", self.update_version)

        self.c.emit("joinProject", [{"project_id": page.project_id}], id=1)
        with gevent.Timeout(5000, False):
            m = self.c.recv()
            self.root_folder =  m["args"][1]["rootFolder"][0] if len(m["args"]) > 1 else None
            self.main_tex = m["args"][1]["rootDoc_id"] if len(m["args"]) > 1 else None
            if self.root_folder:
                page.imgs = [file['_id'] for file in self.root_folder['fileRefs']]
            self.c.emit("joinDoc", [self.main_tex], id=2)
            old_doc = self.c.recv()
            self.doc_text = "\n".join(old_doc["args"][1])
            self.doc_version = old_doc["args"][2]
            self.c.emit("clientTracking.getConnectedUsers", [], id=3)
            self.c.recv()
        assert self.doc_version is not None


    def recv(self): self.c.recv()

    def update_version(self, args):
        rec_ts = current_milli_time()

        if 'client_ts' in args[0] and self.sent_doc_version != args[0]["v"]:
            request_success.fire(request_type='WebSocket',
                                name="update_text",
                                response_time=rec_ts - args[0]['client_ts'],
                                response_length=0)
            # print("update in %s ms" % str(rec_ts - args[0]['client_ts']))

        # if self.sent_doc_version != args[0]["v"]:
        #     print('user %s saw an update it didn\'t emit' % (self.l.parent.email))

        self.doc_version = args[0]["v"]+1
        if self.pending_text is not None:
            self.doc_text = self.pending_text
            self.pending_text = None


    def noop(self, args):
        pass


    pos_triggered = pos_registered = 0
    def on_update_position(self, args):

        rec_ts = current_milli_time()
        if 'client_ts' in args[0] and self.l.parent.email != args[0]['email']:
            request_success.fire(request_type='WebSocket',
                                name="update_cursor_position",
                                response_time=rec_ts - args[0]['client_ts'],
                                response_length=0)
            # print('user %s saw user %s moving at [%s:%s]' % (self.l.parent.email, args[0]['email'], args[0]['row'], args[0]['column']))

            global pos_registered
            pos_registered += 1

        pass

    def on_chat(self, args):
        print('user %s received chat from %s' % (self.l.parent.email, args[0]['user']['email']))
        rec_ts = current_milli_time()
        if 'client_ts' in args[0]:
            request_success.fire(request_type='WebSocket',
                                name="receive_chat_message",
                                response_time=rec_ts - int(args[0]['client_ts']),
                                response_length=0)
        pass

    # def update_document(self, new_text):
    #     update = [ self.main_tex,
    #               {"doc": self.main_tex,
    #                "op": [{"d": self.doc_text, "p":0},
    #                       {"i": new_text, "p":0}],
    #                "v": self.doc_version}]
    #     self.c.emit("applyOtUpdate", update)
    #     self.pending_text = new_text

    def move_and_write(self, text):
        doc_split = self.doc_text.split('\n')
        nr_lines = len(doc_split)
        start_i, end_i= 0, nr_lines-1
        for i in range(0, nr_lines):
            if '\section{Introduction}' in doc_split[i]:
                start_i = i+1
            if '\end{document}' in doc_split[i]:
                end_i = i-1
                break

        if random.randint(1, 50) == 25:
            text += '\n' #add a new line occasionally

        row = random.randint(start_i, end_i)
        col = len(doc_split[row])
        pos = 0
        for j in range(0, row+1):
            pos += len(doc_split[j])+1
        pos -= 1

        # print('user %s moving at [%s:%s]' % (self.l.parent.email, row, col))

        global pos_triggered
        pos_triggered += 1


        dv = self.doc_version
        pos_args = {"row":row,"column":col,"doc_id":self.main_tex}
        doc_args = {"doc":self.main_tex,"op":[{"p":pos,"i":text}],"v":dv}
        self.sent_doc_version = dv
        client_ts = current_milli_time()
        #     client_rid = str(uuid.uuid4().hex)
        pos_args['client_ts'] = client_ts
        doc_args['client_ts'] = client_ts
        #     args[args_i[0]]['client_rid'] = client_rid

        self.c.emit("clientTracking.updatePosition", [pos_args])
        self.c.emit("applyOtUpdate", [self.main_tex, doc_args])
        self.pending_text = self.doc_text[:pos]+text+self.doc_text[pos:]

    def close(self):
        self.c.close()


def template(path):
    with open(os.path.join(ROOT_PATH, path), "r") as f:
        return string.Template(f.read())


def chat(l):
    client_ts = current_milli_time()
    # client_rid = str(uuid.uuid4().hex)
    # l.websocket.c.req_track[client_rid] = dict(name='receive_chat_message', req_ts=client_ts)
    msg = "".join( [random.choice(string.letters) for i in xrange(5)] )
    # p = dict(_csrf=l.csrf_token, content=msg, client_ts=client_ts, client_rid=client_rid)
    # p = dict(_csrf=l.csrf_token, content=msg, client_ts=client_ts)
    p={'_csrf':l.csrf_token, 'content':msg, 'client_ts':client_ts}
    r = l.client.post("/project/%s/messages" % l.project_id, data=p, name="send_chat_message")
    pass

# DOCUMENT_TEMPLATE = template("document.tex")
# def edit_document(l):
#     params = dict(paragraph=random.randint(0, 1000))
#     doc = DOCUMENT_TEMPLATE.safe_substitute(params)
#     l.websocket.update_document(doc)


def move_and_write(l):
    text = ' (hop %s)' % re.findall('\d', l.parent.email)[0]
    l.websocket.move_and_write(text)


def stop(l):
    l.interrupt()


def share_project(l):
    get_contacts(l) #not really used but they go together
    email = "locust%s@sharelatex.dev" % random.randint(1,l.parent.nr_users)
    while email == l.parent.email:
        email = "locust%s@sharelatex.dev" % random.randint(1,l.parent.nr_users)
    p = dict(_csrf=l.csrf_token, email=email, privileges="readAndWrite")
    r = l.client.post("/project/%s/invite" % l.project_id, data=p, name="share_project")
    pass


def share_project_all(l):
    members = json.loads(l.client.get("/project/%s/members" % l.project_id, name="get_project_members").content)['members']
    member_emails = [m['email'] for m in members]

    for i in range(1,l.parent.nr_users+1):
        email = "locust%s@sharelatex.dev" % i
        if email == l.parent.email or email in member_emails:
            continue
        p = dict(_csrf=l.csrf_token, email=email, privileges="readAndWrite")
        r = l.client.post("/project/%s/invite" % l.project_id, data=p, name="share_project")
    pass


def spell_check(l):
    # data = dict(language="en", _csrf=l.csrf_token, words=randomwords.sample(1, 1), token=l.user_id)
    data = dict(language="en", _csrf=l.csrf_token, words=['hello', 'from', 'thi', 'adher', 'sajd'], token=l.user_id)
    # d = {"language":"en","_csrf":l.csrf_token,"words":["hello"],"token":l.user_id}
    # headers = {'Content-Type': 'application/json;charset=UTF-8', 'Accept':'application/json, text/plain, */*', 'Accept-Encoding':'gzip, deflate, br'}
    r = l.client.post("/spelling/check", json=data, name="check_spelling")
    pass


def file_upload(l):
    path = os.path.join(ROOT_PATH, "tech-support.jpg")
    p = dict(folder_id=l.websocket.root_folder['_id'],
             _csrf=l.csrf_token,
             qquuid=str(uuid.uuid1()),
             qqtotalfilesize=os.stat(path).st_size)
    files = { "qqfile": ('tech-support.jpg', open(path, "rb"), 'image/jpeg')}
    resp = l.client.post("/project/%s/upload" % l.project_id, params=p, files=files, name="upload_file")
    pass


def show_history(l):
    r = l.client.get("/project/%s/updates" % l.project_id, params={"min_count": 10}, name="project_updates")
    updates = json.loads(r.content)['updates']
    if len(updates):
        docs = updates[0]['docs']
        first_doc_id = docs.keys()[0]
        u = "/project/%s/doc/%s/diff" % (l.project_id, first_doc_id)
        r = l.client.get(u, params={'from':docs[first_doc_id]['fromV'], 'to':docs[first_doc_id]['toV']}, name="document_diff")
    pass


def compile(l):
    d = {"rootDoc_id": l.websocket.root_folder['_id'] ,"draft": False,"_csrf": l.csrf_token}
    r1 = l.client.post("/project/%s/compile" % l.project_id,
                       json=d,
                       name="compile")
    resp = r1.json()
    if resp["status"] == "too-recently-compiled":
        return
    files = resp["outputFiles"]
    l.client.get("/project/%s/output/output.log" % l.project_id,
            params={"build": files[0]["build"]},
            name="get_compile_log")
    l.client.get("/project/%s/output/output.pdf" % l.project_id,
            params={"build": files[0]["build"], "compileGroup": "standard", "pdfng": True},
            name="get_compile_pdf")


def get_contacts(l):
    r = l.client.get("/user/contacts", name='get_contacts')
    pass


def get_image(l):
    if l.imgs:
        img = random.choice(l.imgs)
        r = l.client.get("/project/%s/file/%s" % (l.project_id, img), name='get_image')
    pass

#
# def find_user_id(doc):
#     # window.csrfToken = "DwSsXuVc-uECsSv6dW5ifI4025HacsODuhb8"
#     user = re.search('window.user_id = \'([^\']+)\'', doc, re.IGNORECASE)
#     assert user, "No user found in response"
#     return user.group(1)
#     # return json.loads(user.group(1))["id"]


def clear_projects(l):
    for p in l.parent.projects:
        clear_project(l, p["id"])


def clear_project(l, project_id):
    l.client.delete("/project/%s" % project_id,
                    params={"_csrf": l.parent.csrf_token},
                    name="delete_project")


def create_project(l, pname):
    d = {"_csrf": l.parent.csrf_token, "projectName": pname, "template": None}
    r = l.client.post("/project/new", json=d, name="create_project")
    return r


def join_projects(l):
    r = l.client.get("/project", name='get_project_list')
    notifications = re.search("\"notifications\":\\[.*\\]", r.content, re.MULTILINE)
    notifications = json.loads('{'+notifications.group(0)+'}')['notifications'] if notifications is not None else []
    csrf_token = csrf.find_in_page(r.content)
    d = {"_csrf": csrf_token}
    projects = re.search("{\"projects\":\\[.*\\]}", r.content, re.MULTILINE)
    projects = json.loads(projects.group(0))['projects'] if projects is not None else []
    pids = [p['id'] for p in projects if not p['archived']]

    for n in notifications:
        p_id = n['messageOpts']['projectId']
        if p_id in pids:
            continue
        token = n['messageOpts']['token']
        resp = l.client.post("/project/%s/invite/token/%s/accept" % (p_id,token), params=d, name="join_project")
        if resp.status_code != 200:
            print('user %s shared %s with %s' % ( n['messageOpts']['userName'], n['messageOpts']['projectName'],l.parent.parent.email))



def get_projects(l):
    r = l.client.get("/project", name='get_project_list')
    projects = re.search("{\"projects\":\\[.*\\]}", r.content, re.MULTILINE)
    projects = json.loads(projects.group(0))['projects'] if projects is not None else []
    return [p for p in projects if not p['archived']]


def set_project(l):
    old_pid = l.project_id if hasattr(l, 'project_id') else None
    join_projects(l)
    projects = get_projects(l)
    l.user_id = l.parent.user_id

    predef = [p for p in projects if p['name'] in l.parent.predef_projects]

    if len(predef)>0:
        projects = predef
    else:
        if len(l.parent.predef_projects) and len(l.parent.predef_projects[0]):
            projects = []
            for pname in l.parent.predef_projects:
                #create these projects and share them with everybody
                new_p = create_project(l, pname).json()
                new_p['id'] = new_p['project_id']
                new_p['name'] = pname
                new_p['owner'] = {'_id':l.user_id}
                # share_project_all(l, new_p['id'])
                projects.append(new_p)

    

    if len(projects):
        l.project = random.choice(projects)
        l.project_id = l.project['id']
        # l.project_id = '5a69b3d3ba0c6d042e460407'
    else:
        pname = randomwords.sample(2, 2)
        pname = "%s %s" % (pname[0], pname[1])
        r = create_project(l, pname)
        l.project = r.json()
        l.project_id = l.project["project_id"]

    l.locust.ws_fwd_path = ''
    # if len(redirect_projs)>0 and l.parent.predef_projects[l.project_id] == 'remote':
    if l.parent.koala_enabled:
            l.locust.ws_fwd_path = 'object/%s/' % l.project_id

    print('User %s is using project %s' % (l.parent.email , l.project['name']))

    if l.project_id != old_pid:
        page = l.client.get("/project/%s" % l.project_id, name="open_project")
        l.csrf_token = csrf.find_in_page(page.content)
        # l.user_id = find_user_id(page.content)

        d = {"shouldBroadcast": False, "_csrf": l.csrf_token}
        res = l.client.post("/project/%s/references/indexAll" % l.project_id, params=d, name="get_references")
        res = l.client.get("/project/%s/metadata" % l.project_id, name="get_project_metadata")


        # if not len(projects):
        # share_project(l)
        # if l.project['owner']['_id'] == l.user_id:
        #     share_project_all(l)

        l.websocket = Websocket(l)
        def _receive():
            try:
                while True:
                    l.websocket.recv()
            except (ConcurrentObjectUseError, WebSocketConnectionClosedException):
                l.interrupt()
                print("websocket closed")
        gevent.spawn(_receive)

# def test_workflow(l):
#
#     share_project(l)
#     for i in range(0, 5):
#         chat(l)
#
#     # for i in range(0, 15):
#     #      l.websocket.move_and_write()
#     #      # spell_check(l)
#     #      time.sleep(1)
#
#
#     spell_check(l)
#     # compile(l)
#     # l.interrupt()
#     os.kill(os.getpid(), signal.SIGINT)



class Page(TaskSet):
    # tasks = { move_and_write: 100, spell_check: 90, compile: 50, chat: 30, show_history: 30, get_image: 8,  share_project: 5, stop: 20}
    tasks = { move_and_write: 100, spell_check: 90, compile: 50, chat: 30, show_history: 30}
    # tasks = { move_and_write: 100, spell_check: 90, stop:10}
    # tasks = { move_and_write: 100}

    def on_start(self):
        set_project(self)

    def interrupt(self,reschedule=True):
        self.websocket.close()
        super(Page, self).interrupt(reschedule=reschedule)