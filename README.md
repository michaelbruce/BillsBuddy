## Bills Buddy

A force.com sublime plugin using neowit's tooling-force.com project

##### Scraps/TODOs

     TODO fix ~ and absolute file paths
     TODO print responseFile too! - code written, untested
     TODO include apex/vf page syntax - WIP, see commented code
     TODO include SuperAnt - optionsin menu
     TODO handle loss of connection/no java/no jar
     TODO allow for multiple bb_paths - requires system/user settings file seperation first
     TODO download latest tooling force if missing + update option + hot update like chrome?
     TODO find tooling-force jar with a methid - os.listdir('.')
     TODO downloader must be threaded too but hold the application until complete..
     TODO invalid/corrupt jar file...
     TODO missing tmp billResponse file? related to missing creds?

     WIP
     class SyntaxHandler(sublime_plugin.EventListener):
         ext = util.get_file_extension(fn)
         try:
             if ext == '.cls' or ext == '.trigger':
                 view.set_syntax_file(os.path.join("Packages","Java","Java.tmLanguage"))
             elif ext == '.page' or ext == '.component':
                 view.set_syntax_file(os.path.join("Packages","HTML","HTML.tmLanguage"))
         except:
             pass

     TODO get actions working on save
     TODO make sure user won't lose focus when this happens
     handles compiling to server on save
     class RemoteEdit(sublime_plugin.EventListener):
         def on_post_save_async(self, view):
             if settings.get('bb_compile_on_save') == True and util.is_mm_file() == True:
                 params = {
                     "files" : [util.get_active_file()]
                 }
                 mm.call('compile', context=view, params=params)
