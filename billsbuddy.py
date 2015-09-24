import sublime, sublime_plugin, os, subprocess, threading
import BillsBuddy.util as util

settings = sublime.load_settings('billsbuddy.sublime-settings')
plugin_path = sublime.packages_path() + '/BillsBuddy'
home_dir = os.path.expanduser('~')

# TODO use os.putenv to find & set JAVAHOME?
# TODO find tooling-force jar with a methid - os.listdir('.')
# TODO create response file from current file name
# TODO end current tooling-force process if call is used again.
# TODO display console when running, auto close after X seconds if successful

class ToolingForce(threading.Thread):
    def __init__(self, args):
        super(ToolingForce, self).__init__()
        sublime.active_window().run_command("show_panel", {"panel": "console"})
        self.args = args

    def run(self):
        command_args = ['java', '-jar', 'tooling-force.com-0.3.4.2.jar',
                        '--config=' + settings.get('bb_config'),
                        '--projectPath=' + settings.get('bb_path'),
                        '--responseFilePath=/tmp/billResponseFile',
                        '--ignoreConflicts=true',
                        '--pollWaitMillis=1000']
        command_args.extend(self.args.split())
        print('Debug: ' + ' '.join(command_args))
        p = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=plugin_path)

        while True:
            buf = p.stdout.readline()
            if not buf:
                break
            print(buf.rstrip().decode("utf-8")),

class BillSaveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        print('=== Pushing to <org_name> ===')
        ToolingForce('--action=deploySpecificFiles')

class BillTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(self.view.file_name()))[0]
        print('=== Running test ' + filename + ' to <org_name> ===')
        t = ToolingForce('--action=runTestsTooling --async=true --testsToRun='
                + filename)
        t.start()

class BillTestSingleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(self.view.file_name()))[0]
        method_name = self.get_current_function(self.view)
        print('=== Running test method ' + method_name + ' to <org_name> ===')
        t = ToolingForce('--action=runTestsTooling --async=true --testsToRun='
                + filename + '.' + method_name)
        t.start()

    def get_current_function(self, view):
            sel = view.sel()[0]
            functionRegs = view.find_by_selector('entity.name.function')
            cf = None
            for r in reversed(functionRegs):
                if r.a < sel.a:
                    cf = view.substr(r)
                    break
            return cf

# TODO get actions working on save
# TODO make sure user won't lose focus when this happens
# #handles compiling to server on save
# class RemoteEdit(sublime_plugin.EventListener):
#     def on_post_save_async(self, view):
#         if settings.get('bb_compile_on_save') == True and util.is_mm_file() == True:
#             params = {
#                 "files" : [util.get_active_file()]
#             }
#             mm.call('compile', context=view, params=params)
#
