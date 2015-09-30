import sublime, sublime_plugin
import os
import subprocess, json
from urllib.request import urlopen

def get_file_extension(filename=None):
    try :
        if not filename: filename = get_active_file()
        fn, ext = os.path.splitext(filename)
        return ext
    except:
        pass
    return None

def get_active_file():
    try:
        return sublime.active_window().active_view().file_name()
    except Exception:
        return ''

def get_current_function(view):
        sel = view.sel()[0]
        functionRegs = view.find_by_selector('entity.name.function')
        cf = None
        for r in reversed(functionRegs):
            if r.a < sel.a:
                cf = view.substr(r)
                break
        return cf

def has_tooling_force():
    if not os.path.isfile(os.path.join(sublime.packages_path(), 'BillsBuddy', 'tooling-force.jar')):
        get_tooling_force()

def get_tooling_force():
    print("Getting latest tooling-force.com release from github...")

    proc = subprocess.Popen(["curl",
        "https://api.github.com/repos/neowit/tooling-force.com/releases"],
        stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    url = (json.loads(out.decode())[0]['assets'][0]['browser_download_url'])
    file_name = 'tooling-force.jar'
    u = urlopen(url)
    f = open(os.path.join(sublime.packages_path(), 'BillsBuddy', 'tooling-force.jar'), 'wb')
    meta = u.info()
    file_size = int(meta['Content-Length'])
    print("Downloading: %s Bytes: %s" % (file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        print (status),

    f.close()
