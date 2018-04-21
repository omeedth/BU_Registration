import time
import re;
import config;

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Global Variables

year = ''
regop = []
regchoice = ''
reg_choice = None
course_selected = False

chc = 0;
old_course_information = []
new_course_section = ''

# Fuctions

def get_reg_options():
    #regops = driver.find_elements_by_link_text('Reg Options')
    regops = driver.find_elements_by_xpath("//tbody//td[contains(text(),'"+ year +"')]")
    print('There are ' + str(len(regops)) + ' registrations options!\n')
    return regops

def print_text(webelements):
    for webelement in webelements:
        print('text: ' + webelement.text + '\n')

def print_strings(strings):
    print('text:\n')
    for string in strings:
        print(string + '\n')

def web_to_str(webelements):
    webelements_str = []
    for webelement in webelements:
        webelements_str += [str(webelement.text[0:14]).split('20')[0].strip()]
        #print('added: ' + webelement.text)
    return webelements_str

def sign_in():
    username = config.DATACOUP_USERNAME;
    password = config.DATACOUP_PASSWORD;

    login_user = driver.find_element_by_id('j_username')
    login_pass = driver.find_element_by_id('j_password')
    login_btn = driver.find_element_by_name('_eventId_proceed')

    login_user.send_keys(username)
    login_pass.send_keys(password)
    login_btn.click()

def accept_alert():
    #respond to alert if there is one
    try:
        WebDriverWait(driver, 0.5).until(EC.alert_is_present(),
                                           'Timed out waiting for PA creation ' +
                                           'confirmation popup to appear.')

        alert = driver.switch_to.alert
        alert.accept()
        print("alert accepted")
        driver.back()
        driver.back()
    except:
        print('No Alert Found!')
        driver.back()

def advising_code():
    while 1:
        try:
            advising_cd = driver.find_element_by_name('AdvisingCd')
            unlock = driver.find_element_by_xpath("//input[@value='Unlock']")
            cd = str(input('What\'s the advising code: '))
            advising_cd.clear()
            advising_cd.send_keys(cd)
            time.sleep(0.5)
            unlock.click()
        except:
            print('No advising code needed!!!')
            break

        try:
            WebDriverWait(driver, 1).until(EC.alert_is_present(),
                               'Timed out waiting for PA creation ' +
                               'confirmation popup to appear.')

            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
            continue
        except TimeoutException:
            print("no alert")

        try:
            driver.find_element_by_tag_name('b').text
        except Exception:
            register_for_class = driver.find_element_by_link_text('Register for Class')
            break

        print('Incorrect Advising Code!\n\'Ctrl+C\' to quit program!')

        driver.find_element_by_link_text('Back').click()     

def access_reg_options(choice):
    #1: plan
    #2: register
    #3: drop
    #4: change section

    link = None

    options = ['None','Plan','Register for Class','Drop Class','Change Section']

    if choice >= len(options) or choice < 1:
        print('No such option')
        return False
        
    try:
        link = driver.find_element_by_link_text(options[choice])
        link.click()
    except:
        print('Link Not Found!\nType in Advising Code...')
        advising_code()
        link = driver.find_element_by_link_text(options[choice])
        link.click()

    return True

def search_by_class_num():
    college = driver.find_element_by_name('College')    #Dropdown
    department = driver.find_element_by_name('Dept')    #text
    course = driver.find_element_by_name('Course')      #text
    section = driver.find_element_by_name('Section')    #text    

    clg = str(input('Which college are you in: ').upper())
    dept = str(input('Which department do you want to search for: '))
    crse = str(input('Which course do you want to search for: '))
    sect = str(input('Which section do you want to search for: '))

    #option
    option = driver.find_element_by_xpath("//option[contains(text(), '%s')]" % clg)   #Option
    
    #dropdown
    college.click()
    option.click()

    #department
    department.send_keys(dept)

    #course
    course.send_keys(crse)

    #section
    section.send_keys(sect)

    #search
    #go.click()
    college.submit()
    
    return [clg,dept,crse,sect]

def find_and_select_course(lst):
    """From here I want to repeatedly refresh the page until the
    course I want is available and click finish"""

    clg = lst[0]
    dept = lst[1]
    crse = lst[2]
    sect = lst[3]
    
    while 1:        

        try:
            
            sign_in()
            
            academics = driver.find_element_by_css_selector("a img[alt='Academics']")
            academics.click()
            registration = driver.find_element_by_link_text('Registration')
            registration.click()

            #Registration Choices!
            print('Locating previous registration options...')
            regop = get_reg_options()           
              
            for reg in regop:
                if regchoice in reg.text:
                    reg_choice = reg            
                    break    

            print('Registration Choice: ' + regchoice)

            reg_choice.find_element_by_link_text('Reg Options').click()

            #Accessing reg options
            access_reg_options(chc)
            
        except:
            pass            
        
        try:
            classes = driver.find_elements_by_partial_link_text(clg.upper() + ' ' + dept.upper() + crse + ' ' + sect.upper())
        
        except Exception:
            print('Couldn\'t Find Class!')
            break

        print('classes: ' + str(len(classes)) + '\n')

        course_selected = False

        for course in classes:
            #Class info
            tr = course.find_element_by_xpath('../..')
            print('this tag is: ' + str(tr.text) + '\n')            
            add_course = None
            try:
                add_course = tr.find_element_by_tag_name('input')
            except Exception:
                print('No add course check box found!')
            title = tr.find_element_by_css_selector("td:nth-child(4)")
            open_seats = tr.find_element_by_css_selector("td:nth-child(6)")
            type_class = tr.find_element_by_css_selector("td:nth-child(8)")
            
            print('\ntitle: ' + title.text)
            print('open seats: ' + open_seats.text)
            print('class type: ' + type_class.text)

            if open_seats != '0' and add_course != None:
                try:
                    #btn = add_course.find_element_by_tag_name('input')
                    """
                    if add_course.is_selected():
                        add_course.submit()
                        break
                    """
                    add_course.click()
                    course_selected = True
                except Exception:
                    print('No add course button found!')

        if course_selected:
            add = driver.find_element_by_xpath("//center[2]/table/tbody/tr/td[1]/input").click()
            print('\nAdded A Class!\n')
            break
        #driver.find_element_by_name("s").sendKeys(Keys.F5);
        driver.refresh()
        print('\nRefreshed Page\n')

    #respond to alert if there is one
    accept_alert()
    old_course_information = None
    new_course_section = ''
    

def add_from_planner():
    # In Planner
    planner = driver.find_element_by_css_selector("input[onclick='SearchPlanner()']")
    planner.click()

    #Cycle through all available classes in planner and check mark
    check_boxes = driver.find_elements_by_css_selector("input[type='checkbox'][name='SelectIt']")
    for check_box in check_boxes:
        check_box.click()

    #Add checkmarked classes to schedule
    add_classes = driver.find_element_by_css_selector("input[onclick='AddClasses();']")
    add_classes.click()

    #respond to alert if there is one
    accept_alert()

def plan():
    add = driver.find_element_by_link_text('Add')
    add.click()
    find_and_select_course(search_by_class_num())

def register():

    while True:
        print('(1) Add from planner')
        print('(2) Add from search')
        choice = int(input('Make a choice: '))

        if choice in range(1,3):
            break

        print('Invalid input!\nEither 1 or 2')

    if choice == 1:
        try:
            add_from_planner()
        except:
            print('Unable To Add From Planner!')
    elif choice == 2:
        try:
            find_and_select_course(search_by_class_num())
        except:
            print('Unable To Add By Selecting and Searching!')

def drop():
    print('Not implemented!')
    
def change():
    print('Enter details of class you would like to change!\n')
    clg = str(input('Which college are you in: ').upper())
    dept = str(input('Which department are you in: '))
    crse = str(input('Which course are you in: '))
    sect = str(input('Which section are you in: '))

    if clg == '' or dept == '' or crse == '' or sect == '':
        print('You did not input all of the fields you needed!')
        return

    try:
        class_c = driver.find_element_by_partial_link_text(clg.upper() + ' ' + dept.upper() + crse + ' ' + sect.upper())
        class_c.click()
    except:
        print('You are not in course: \'' + clg.upper() + ' ' + dept.upper() + crse + ' ' + sect.upper() + '\'')
        return

    old_course_information = [clg, dept, crse, sect]

    sect = str(input('Enter the new section you would like to enter: '))

    new_course_section = sect;

    while 1:

        try:
            sign_in()
            #academics = driver.find_element_by_link_text('Academics')
            academics = driver.find_element_by_css_selector("a img[alt='Academics']")
            academics.click()
            registration = driver.find_element_by_link_text('Registration')
            registration.click()

            print('Locating previous registration options...')
            
            #Registration Choices!        
            regop = get_reg_options()           
              
            for reg in regop:
                if regchoice in reg.text:
                    reg_choice = reg            
                    break    

            print('Registration Choice: ' + regchoice)

            reg_choice.find_element_by_link_text('Reg Options').click()

            #Go back to previous registration option
            access_reg_options(chc)

            link = driver.find_element_by_link_text(clg.upper() + ' ' + dept.upper() + crse + ' ' + sect.upper())
            link.click()
            
        except:
            pass            

        try:
            link = driver.find_element_by_link_text(clg.upper() + ' ' + dept.upper() + crse + ' ' + sect.upper())
            link.click()
            break
        except:            
            driver.refresh()

    accept_alert()
    old_course_information = None
    new_course_section = ''
    
# Main

driver = webdriver.Chrome('chromedriver.exe')

driver.implicitly_wait(.5) # seconds

driver.get('https://www.bu.edu/link/bin/uiscgi_studentlink.pl/1519065025?ModuleName=menu.pl&NewMenu=Academics')

registration_link = driver.find_element_by_link_text('Registration')
registration_link.click()

login = driver.find_element_by_tag_name('h1')

if login != None:
    print('\nThis is the login page!\nLogging In...')
    sign_in()

print('Logged In!')

while 1:

    while 1:
        try:
            year = str(input('\nPick a year for your registration options: '))

            #Registration Choices!
            print('\nYour Registration Options are:\n')
            regop = get_reg_options()
            if len(regop) > 0:
                break
        except Exception:
            print('Year invalid!\n')

    regop_str = web_to_str(regop)
    print(str(regop_str))

    while 1:
        regchoice = str(input('Which registration would you like to go to: '))
        if regchoice in regop_str:
            print('\nValid Input!\n')
            break
        else:
            pass

    for reg in regop:
        if regchoice in reg.text:
            reg_choice = reg
            print('Found your selected register option!\n')
            break    

    reg_choice.find_element_by_link_text('Reg Options').click()

    # Home registering page

    print('--Reminder-- Registration Choice: ' + regchoice + '\n')

    while True:
        print('(1) Plan')
        print('(2) Register for Class')
        print('(3) Drop Class')
        print('(4) Change Section')
        choice = int(input('Please choose a link: '))
        chc = choice

        if access_reg_options(choice):
            if choice == 1:
                plan()
            elif choice == 2:
                register()
            elif choice == 3:
                drop()
            elif choice == 4:
                change()

        print('(1) Go Back to Registration Options')
        print('(2) Go Back to Registration - Current Schedule')
        print('(Anything Else) To quit')
        try:
            choice = int(input('Please choose: '))
        except:
            print('Exiting Program...')
            exit()

        if choice == 1:
            title = driver.find_element_by_tag_name('b')
            while title.text != 'REGISTRATION OPTIONS':
                driver.back()
                title = driver.find_element_by_tag_name('b')
        elif choice == 2:
            title = driver.find_element_by_tag_name('b')
            while title.text != 'REGISTRATION - CURRENT SCHEDULE':
                driver.back()
                title = driver.find_element_by_tag_name('b')
            break
        else:
            print('Exiting Program...')
            exit()
