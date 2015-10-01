#!/usr/bin/env python

from os.path import expanduser

def dummy_get_active_file():
    return '/Users/mikepjb/Workspace/Singletrack-Core/Singletrack-Revenue-And-Orders'

json_with_project_list = {"bb_projects": [
    {"path" : "~/Workspace/Singletrack-Core/SingletrackDev",
        "username" : "devboy@st.com",
        "password" : "",
        "security_token" : ""},
    {"path" : "~/Workspace/Singletrack-Core/Singletrack-Revenue-And-Orders",
        "username" : "reverend@st.com",
        "password" : "",
        "security_token" : ""},
    ]}

for project in json_with_project_list['bb_projects']:
    if expanduser(project['path']) in dummy_get_active_file():
        print('found matching path for the user' + project['username'])
