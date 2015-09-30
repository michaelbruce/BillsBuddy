import sublime, sublime_plugin, os, subprocess, threading
from BillsBuddy import util

class ToolingForce(threading.Thread):
    def __init__(self, args):
        self.settings = sublime.load_settings('billsbuddy.sublime-settings')
        self.plugin_path = sublime.packages_path() + '/BillsBuddy'
        super(ToolingForce, self).__init__()
        sublime.active_window().run_command("show_panel", {"panel": "console"})
        self.args = args

    def run(self):
        util.has_tooling_force()
        command_args = ['java', '-jar', 'tooling-force.jar',
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
        filename = os.path.basename(util.get_active_file())
        print('=== Pushing ' + filename + ' to SingletrackDev ===')
        self.create_meta_file()
        t = ToolingForce('--action=deploySpecificFiles --specificFiles=/tmp/currentFile')
        t.start()

    def create_meta_file(self):
        filename = util.get_active_file().split('SingletrackDev/')[1]
        meta_file = open('/tmp/currentFile', 'w')
        meta_file.write("{0}\n{0}-meta.xml".format(filename))

class BillTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(util.get_active_file()))[0]
        print('=== Running test ' + filename + ' to SingletrackDev ===')
        t = ToolingForce('--action=runTestsTooling --async=true --testsToRun='
                + filename)
        t.start()

class BillTestSingleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(self.view.file_name()))[0]
        method_name = self.get_current_function(self.view)
        print('=== Running test method ' + method_name + ' to SingletrackDev ===')
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
