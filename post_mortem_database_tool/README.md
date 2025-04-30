# Post-mortem Database Tool
Developping a post-mortem for logging, tracking, and reviewing the results for activities.

### Strategic Plan
* Using python to develop a gui for this tool. And using the file system to organize the data. 
* Plan to using [tkinter](https://docs.python.org/3/library/tkinter.html) to build the GUI.
* On the data organize side, there will be two major objects, Project and Record.
* This tool is project based, the GUI will only support open one project at once. And in the project there can be as many records as needed. 
* The data organize will be build based on the normal file system. Each project will be a folder, all the records and other info will be stored in the project folder. And there will be a json file to tracking all the records.
* Each record will be a folder under the project. Inside the record folder, will have the json file to handle all the record infomation. all the logging files upload to the record will be stored in this folder and tracked by the json file too.
* On the GUI
    * there will be a tool bar on the top to create, open and close project.
    * when opened a project, the project name will shows on the title of the window.
    * on the left side, it shows the list of the records, and user can select one of those record.
    * on the bottom of the records list, there is a add new button to adding new records.
    * when click the add new button, it will open a new window to let user enter new records. 
        * The new window will have a save button to close and save the record, and a cancel button to give up the adding
    * on the right side, it will shows the selected records. on the buttom will be a edit button.
    * when click the edit button, it will shows the same new record window, with the old data filled.
    * the record will contain title, date, report, and logging files.

### Run tools
* first install python, I am using python 3.13 on macOS
* install depedences package
    ```
    python -m pip install tkinterdnd2
    ```
* Run project
    ```
    python post_mortem_tool.py
    ```

### Tools
* VS Code: the text editor.
* python: programming.
* git: storage.
* google and ChatGPT: for searching, and coding help.