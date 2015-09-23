import sublime, sublime_plugin, os

settings = sublime.load_settings('billsbuddy.sublime-settings')
plugin_path = sublime.packages_path()
home_dir = os.path.expansuser('~')

# TODO use os.putenv to find & set JAVAHOME?
# TODO find tooling-force jar with a methid - os.listdir('.')

class ToolingForce:
    def call(args):
        # TODO create response file from current file name
        # TODO end current tooling-force process if call is used again.
        # TODO how to reference $HOME in python?
        p = os.popen("echo hiiii")
        os.popen(("java -jar tooling-force.com-0.3.4.2.jar"
            " --config=" + home_dir + settings.get('bb_config')
            " --projectPath=" + home_dir + settings.get('bb_path')
            " --responseFilePath=/tmp/billResponseFile"
            " --ignoreConflicts=true"
            " --pollWaitMillis=1000")
        #now wait & print

class BillHelpCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ToolingForce.call('--help')
        # self.view.insert(edit, 0, "Hello, World!")

class BillSaveCeommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = sublime.Window.active_view(sublime.active_window())
        # print view.run_command("delete_current_file")
        print(os.popen(("java -jar ' . $HOME . '/dotfiles/tooling-force.com-0.3.4.2.jar"
                        " --action=deploySpecificFiles"
                        "--config=' . $HOME . '/notes/SingletrackDev.properties"
                        "--projectPath=' . $HOME . '/Workspace/Singletrack-Core/SingletrackDev"
                        "--responseFilePath=/tmp/responseFile"
                        "--specificFiles=/tmp/currentFile"
                        "--ignoreConflicts=true"
                        "--pollWaitMillis=1000")).read())

# function! ApexDeployCurrent()
#   let term = GetTerm()
#   let newFile = substitute(expand('%'), $HOME . 'Workspace/Singletrack-Core/SingletrackDev','','')
#   exec ':!echo -e "' . newFile . '\n' . newFile . '-meta.xml" > /tmp/currentFile'
#   exec term . 'java -jar ' . $HOME . '/dotfiles/tooling-force.com-0.3.4.0.jar
#         \ --action=deploySpecificFiles
#         \ --config=' . $HOME . '/notes/SingletrackDev.properties
#         \ --projectPath=' . $HOME . '/Workspace/Singletrack-Core/SingletrackDev
#         \ --responseFilePath=/tmp/responseFile
#         \ --specificFiles=/tmp/currentFile
#         \ --ignoreConflicts=true
#         \ --pollWaitMillis=1000'
# endfunction
