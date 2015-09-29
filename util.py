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

