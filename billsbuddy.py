import sublime, sublime_plugin

settings = sublime.load_settings('billsbuddy.sublime-settings')
plugin_path = sublime.packages_path()

import subprocess
from subprocess import Popen,PIPE
import os


class ToolingForce:
    def call(args):
        p = subprocess.Popen("echo hiiii")
        p.communicate() #now wait

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
