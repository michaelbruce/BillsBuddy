# def is_salesforce_file(filename=None):
#     try:
#         if is_mm_project():
#             if not filename:
#                 filename = get_active_file()
#             project_directory = mm_project_directory(sublime.active_window())
#             if os.path.join(project_directory,"src","documents") in filename:
#                 return True
#             if os.path.exists(filename) and os.path.join(project_directory,"src") in filename:
#                 valid_file_extensions = settings.get("bb_apex_file_extensions", [])
#                 if get_file_extension(filename) in valid_file_extensions and 'apex-scripts' not in get_active_file():
#                     return True
#                 elif "-meta.xml" in filename:
#                     return True
#     except Exception as e:
#         pass
#     return False
import sublime
import os
import subprocess, json
from urllib.request import urlopen

packages_path = sublime.packages_path()
bills_path = packages_path + '/BillsBuddy/'


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
    print('hiii')
    print(os.getcwd())
    print('bills path: ' + str(bills_path))
    if not os.path.isfile(bills_path + 'tooling-force.jar'):
        print("location:" + str(os.getcwd()))
        get_tooling_force()

def get_tooling_force():
    print("Getting latest tooling-force.com release link from github...")

    proc = subprocess.Popen(["curl", "https://api.github.com/repos/neowit/tooling-force.com/releases"], stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    print("Downloading...")

    url = (json.loads(out.decode())[0]['assets'][0]['browser_download_url'])
    file_name = 'tooling-force.jar'
    u = urlopen(url)
    f = open(bills_path + file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
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
        status = status + chr(8)*(len(status)+1)
        print (status),

    f.close()
