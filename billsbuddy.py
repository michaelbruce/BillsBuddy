import sublime, sublime_plugin, os, subprocess, threading

settings = sublime.load_settings('billsbuddy.sublime-settings')
plugin_path = sublime.packages_path() + '/BillsBuddy'
home_dir = os.path.expanduser('~')

# TODO use os.putenv to find & set JAVAHOME?
# TODO find tooling-force jar with a methid - os.listdir('.')
# TODO create response file from current file name
# TODO end current tooling-force process if call is used again.

class ToolingForce(threading.Thread):
    def __init__(self, args):
        super(ToolingForce, self).__init__()
        self.args = args

    def run(self):
        print('got here')
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
            try:
                buf = p.stdout.readline()
                if not buf:
                    break
                print(buf.rstrip().decode("utf-8")),
            except KeyboardInterrupt:
                break

class BillSaveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ToolingForce('--action=deploySpecificFiles')

class BillTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        t = ToolingForce('--action=runTestsTooling --async=true --testsToRun='
                + os.path.splitext(os.path.basename(self.view.file_name()))[0])
        t.start()

class BillTestSingleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        t = ToolingForce('--action=runTestsTooling --async=true --testsToRun='
                + os.path.splitext(os.path.basename(self.view.file_name()))[0]
                + '.' + self.get_current_function(self.view))
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
