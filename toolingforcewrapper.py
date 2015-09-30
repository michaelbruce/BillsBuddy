import sublime, sublime_plugin, os, subprocess, threading
from BillsBuddy import util

class ToolingForceWrapper(threading.Thread):
    def __init__(self, args):
        self.settings = sublime.load_settings('billsbuddy.sublime-settings')
        self.plugin_path = sublime.packages_path() + '/BillsBuddy'
        super(ToolingForceWrapper, self).__init__()
        sublime.active_window().run_command("show_panel", {"panel": "console"})
        self.args = args

    def run(self):
        util.has_tooling_force()
        command_args = ['java', '-jar', 'tooling-force.jar',
                        '--config=' + expanduser(self.settings.get('bb_config')),
                        '--projectPath=' + expanduser(self.settings.get('bb_path')),
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

        print(open('/tmp/billResponseFile','r').read())

