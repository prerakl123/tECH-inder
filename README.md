# tECH-inder
`tECH-inder` or tinder for **tech** is a recruitment platform for all the students and project makers who wish to create great projects for a great future.

## Pre-requisites
- Windows 10
- Should have Python installed (recommended Python version >=Python3.9)
- Web Browser (any latest browser with JavaScript enabled)

## Installation and setup
- Install the project as zip file from the download option provided by GitHub.
- Run the setup.ps1 file on Windows CMD or PowerShell
- If PowerShell shows an error like the following

    [![ps1 script running error](https://github.com/prerakl123/tECH-inder/blob/main/pics/ps1%20script%20running%20error.png)](https://raw.githubusercontent.com/prerakl123/tECH-inder/main/pics/ps1%20script%20running%20error.png)

    execute the following command:
    ```ps1
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    ```
    
    then run setup.ps1:
    ```ps1
    .\setup.ps1
    ```
- The setup (if successful) usually takes a few minutes and might look like it's stalled or nothing is happening so unless you see a flask message in your command line somewhat like:
    ```ps1
     * Serving Flask app 'techinder.py'
     * Debug mode: off
    WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
     * Running on http://127.0.0.1:5000
    Press CTRL+C to quit
    ```

## Running on localhost
If the project has already been installed, then you can run it inside the virtual environment (venv):
  - To activate the virtual environment, go to your techinder root folder and type the following:
    ```ps1
    .\venv\Scripts\activate
    ```
  If an error occurs like the one mentioned above in the [Installation and Setup](https://github.com/prerakl123/tECH-inder/edit/main/README.md#installation-and-setup) of the project, then the same previously mentioned command has to be executed:
    ```ps1
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
    ```
  Now run the virtual environment activate command again.
  > The command line should now look like this:
  >  ```ps1
  >   (venv) C:\your_folder_path_to_techinder\
  >  ```
  After successfully activating the venv run the flask app by using:
  ```ps1
  flask run
  ```
  If there was no error, now all you need to do is to go to your browser and type `http://localhost:5000` or `http://127.0.0.1:5000`
  
### Testing the app
After successfully running the `flask run` command and opening the flask app in the browser, try registering with different values, signing-in, testing browser back button, view profile section, logging-out, etc; play around with updating account details, profiles, etc as well as creating different scenarios for the app to work and do report possible loop holes and bugs.

**IF YOU ENCOUNTER AN ERROR DO REPORT THE ISSUE** _[HERE](https://github.com/prerakl123/tECH-inder/issues)_
**. IT NOT ONLY HELPS DEVELOP A BETTER PROJECT BUT ALSO HELPS WITH GAINING KNOWLEDGE MUTUALLY.**
