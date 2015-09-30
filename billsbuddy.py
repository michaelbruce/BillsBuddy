import sublime, sublime_plugin, os, subprocess, threading
import BillsBuddy.util as util

# TODO print responseFile too! - code written, untested
# TODO include apex/vf page syntax - WIP, see commented code
# TODO include SuperAnt - optionsin menu
# TODO handle loss of connection/no java/no jar
# TODO allow for multiple bb_paths - requires system/user settings file seperation first
# TODO download latest tooling force if missing + update option + hot update like chrome?
# TODO find tooling-force jar with a methid - os.listdir('.')

class ToolingForce(threading.Thread):
    def __init__(self, args):
        self.settings = sublime.load_settings('billsbuddy.sublime-settings')
        self.plugin_path = sublime.packages_path() + '/BillsBuddy'
        super(ToolingForce, self).__init__()
        sublime.active_window().run_command("show_panel", {"panel": "console"})
        self.args = args

    def run(self):
        command_args = ['java', '-jar', 'tooling-force.com-0.3.4.2.jar',
                        '--config=' + self.settings.get('bb_config'),
                        '--projectPath=' + self.settings.get('bb_path'),
                        '--responseFilePath=/tmp/billResponseFile',
                        '--ignoreConflicts=true',
                        '--pollWaitMillis=1000']
        command_args.extend(self.args.split())
        print('Debug: ' + ' '.join(command_args))
        p = subprocess.Popen(command_args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=self.plugin_path)

        while True:
            buf = p.stdout.readline()
            if not buf:
                break
            print(buf.rstrip().decode("utf-8")),

        print(open('/tmp/billResponseFile','r'))


class BillDeployCommand(sublime_plugin.TextCommand):
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
        util.has_tooling_force()
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


# WIP
# class SyntaxHandler(sublime_plugin.EventListener):
#     ext = util.get_file_extension(fn)
#     try:
#         if ext == '.cls' or ext == '.trigger':
#             view.set_syntax_file(os.path.join("Packages","Java","Java.tmLanguage"))
#         elif ext == '.page' or ext == '.component':
#             view.set_syntax_file(os.path.join("Packages","HTML","HTML.tmLanguage"))
#     except:
#         pass

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
