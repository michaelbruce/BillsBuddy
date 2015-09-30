import sublime, sublime_plugin, os
from os.path import expanduser
from BillsBuddy import util

class BillDeployCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.basename(util.get_active_file())
        print('=== Pushing ' + filename + ' to SingletrackDev ===')
        self.create_description_file()
        ToolingForceWrapper('--action=deploySpecificFiles --specificFiles=/tmp/currentFile').start()

    def create_description_file(self):
        filename = util.get_active_file().split('SingletrackDev/')[1]
        description_file = open('/tmp/currentFile', 'w')
        description_file.write("{0}\n{0}-meta.xml".format(filename))

class BillTestCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(util.get_active_file()))[0]
        print('=== Running test ' + filename + ' to SingletrackDev ===')
        ToolingForceWrapper('--action=runTestsTooling --async=true --testsToRun='
                     + filename).start()

class BillTestSingleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = os.path.splitext(os.path.basename(self.view.file_name()))[0]
        method_name = self.get_current_function(self.view)
        print('=== Running test method ' + method_name + ' to SingletrackDev ===')
        ToolingForceWrapper('--action=runTestsTooling --async=true --testsToRun='
                     + filename + '.' + method_name).start()

    def get_current_function(self, view):
            sel = view.sel()[0]
            functionRegs = view.find_by_selector('entity.name.function')
            cf = None
            for r in reversed(functionRegs):
                if r.a < sel.a:
                    cf = view.substr(r)
                    break
            return cf
