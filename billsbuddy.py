import sublime, sublime_plugin, os, subprocess

settings = sublime.load_settings('billsbuddy.sublime-settings')
plugin_path = sublime.packages_path() + '/BillsBuddy'
home_dir = os.path.expanduser('~')

# TODO use os.putenv to find & set JAVAHOME?
# TODO find tooling-force jar with a methid - os.listdir('.')

class ToolingForce:
    def call(args):
        # TODO create response file from current file name
        # TODO end current tooling-force process if call is used again.
        # TODO paths and spaces...
        command_args = ['java', '-jar', 'tooling-force.com-0.3.4.2.jar',
                        '--config=' + settings.get('bb_config'),
                        '--projectPath=' + settings.get('bb_path'),
                        '--responseFilePath=/tmp/billResponseFile',
                        '--ignoreConflicts=true',
                        '--pollWaitMillis=1000']
        command_args.extend(args.split())
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

class BillHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ToolingForce.call('--help')

class BillSaveCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ToolingForce.call('--action=deploySpecificFiles')
