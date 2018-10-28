# BU_Registration
Helps register for classes by continuously refreshing the page and selecting the desired class!
This is not perfectly optomized yet so it will be finnicky.

# Installing

1. Clone the repository
   * Create a folder dedicated for this
   * Download the all the files in the folder you created
2. Install Selenium
   * Install Selenium using pip
     * ``` pip install selenium ```
     * pip is a python package installer! <br />
     if you don't have it you should get it because it is useful!
     https://pypi.org/project/pip/  
   * Additional Information:
     * http://selenium-python.readthedocs.io/installation.html
    
3. Modify config.py
![config.py](https://github.com/omeedth/BU_Registration/blob/master/config_py.png)
    * Type in your Boston University login name and password for the two respective variables

4. (Optional) Add to Path
If you are on a Windows computer you can right click on the "SetupRegister.cmd" and "run as administrator".
This will add this folder to the path for you! Alternatively you may get the path to the folder containing all of these files and add it yourself. Here is a link explaining how to add an environment PATH variable: https://docs.telerik.com/teststudio/features/test-runners/add-path-environment-variables

# Running
1. Open the file named "RegistrationScript_Clean.py"
2. Follow the command prompt that is created

# Alternative Run
1. (Windows Only) Using Batch File
You may run the "register.bat" script to run the program! (This will only work if you added this as a PATH variable)

# Built With
1. Selenium

# Additional Notes
Please feel free to ask any questions or introduce any problems you would like to be addressed with the script

# FAQ

1. I followed the steps but nothing is happening when I run the script!
    * Make sure you are running the installation of python that has Selenium installed 
