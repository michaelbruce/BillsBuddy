## Bills Buddy

A sublime plugin used to deploy and test files on salesforce.

It uses neowit's tooling-force.com project to do this.

##### Installation instructions

1. Press `cmd + shift + p` to bring up sublime commands prompt.
2. Type `add repo` and paste this link in: `https://github.com/michaelbruce/BillsBuddy.git`
3. Press `cmd + shift + p` again.
4. This time, type in `install package` and search for BillsBuddy.

At this point BillsBuddy will be installed, now you need to create a build.properties file to start using it. It should be a text file containing the following lines:

> sf.username = username@companyname.com  
> sf.password = password_with_security_token  
> sf.serverurl = https://login.salesforce.com 

Finally, select `Configure Settings` the BillsBuddy dropdown and change the `bb_config` option to point at the location of your build.properties file.

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
