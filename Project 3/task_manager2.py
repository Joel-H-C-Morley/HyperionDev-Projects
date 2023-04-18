# ================Importing libraries================

from datetime import date
from datetime import datetime

# ================Functions================

# Registering a new user (admin only)
def reg_user_admin(name_list):

    # Loop to ensure only a NEW username is entered
    while True:

        # User enters new username
        new_uname = input("Enter new username: ")
        if new_uname not in name_list:

            # Loop to ensure user enters the same new password
            while True:

                new_pword = input("Enter new password: ")
                confirm_pword = input("Confirm new password: ")

                if new_pword == confirm_pword:

                    # Matching passwords are added to database, global variable names updated
                    names = name_list.append(new_uname)
                    with open('user.txt', 'a') as f:
                        f.write('\n' + new_uname + ', ' + new_pword)
                    print(f"Added user: {new_uname} and password: {new_pword}")
                    break

                else:

                    # Non-matching passwords give error, will return to input prompt
                    print("Error: Passwords do not match")
                    continue
            break
        else:
            # Update global variable and return so when query is run again, names are updated
            names = name_list
            print("User name already taken")
            continue
    return names


# Creating a new task
def add_task():

    # Prompt user to input details of new task
    user = input("Username of the person whom the task is assigned to: ")
    title = input("Title of task: ")
    description = input("Brief task description: ")
    due = input("Due date of task: ")
    today = date.today()
    status = input("Is task complete?: ")

    # Write new task to file
    with open("tasks.txt", "a") as f:
        f.write(f'\n{user}, {title}, {description}, {today.strftime("%d %b %Y")}, {due}, {status}')


# View all tasks
def view_all():

    task_dict = create_task_dictionary()

    # Iterate through list of tasks and print task information for each task
    for i in range(len(task_dict)):
        print_tasks(task_dict, i)


# View tasks that belong to logged-in user
def view_mine(user):

    task_dict = create_task_dictionary()

    # Loop to ensure menu choice is properly selected
    while True:
        try:

            # Display task number and title of user's tasks
            print(f'-------------------------------------------------------\nTask Number\t-\tTask')
            for i in range(len(task_dict)):
                # Print names of user's tasks
                if user == task_dict[i][0]:
                    print(f'\t{i}\t\t:\t{task_dict[i][1]}')
            print('------------------------------------------------------')

            # Get user's task choice and open submenu, or exit
            task_selection = int(input('Select task to view, or type -1 to return to menu: '))
            if task_selection == -1:
                pass
            else:
                view_mine_submenu(task_selection)
            break

        except ValueError:
            print("Check your menu choice")
            continue


# View task details, update complete status, change task owner
def view_mine_submenu(task_selection):

    task_dict = create_task_dictionary()

    # Loop to ensure only a choice form the menu is selected
    while True:

        # Ask user to choose to view task details, edit task or update task status
        edit_or_mark = input('''Select one of the following options below:
            v - view task details
            m - Update task status to 'complete'
            ed - Edit task
            -1 - Return to menu
            : ''').lower()

        # Option1: Print task information for tasks matching the logged-in user's username
        if edit_or_mark == 'v':
            print_tasks(task_dict,task_selection)

        # Option2: Flip the task status to complete (only works in positive direction, cannot change to 'incomplete')
        elif edit_or_mark == 'm':
            task_dict[task_selection][5] = 'Yes'
            print(f'Task {task_selection} marked as \'complete\'')
            break

        # Option3: Edit task
        elif edit_or_mark == 'ed' and task_dict[task_selection][5].lower() == 'no':

            # Loop to ensure 'edit task' submenu option is chosen correctly
            while True:

                #User inputs submenu choice
                owner_or_date = input('''Select one of the following options below:
                    t - task owner
                    d - due date
                    : ''').lower()

                # Change name of task owner
                if owner_or_date == 't':
                    task_dict[task_selection][0] = input('Enter username of task\'s new owner: ')
                    break

                # Change the due date of task
                elif owner_or_date == 'd':
                    task_dict[task_selection][4] = input('Enter new due date in \'dd Mon yyyy\' format: ')
                    break

                # Stay in loop until correct menu option is chosen
                else:
                    print("Enter only one of the options, completed tasks cannot be edited")

            break

        # Exit the menu
        elif edit_or_mark == '-1':
            break
        # Stay in loop until correct menu option is chosen
        else:
            print("Enter only one of the options")

    # Write updated tasks to file (re-write whole database)
    with open("tasks.txt", "w") as f:
        for i in range(len(task_dict)):
            f.write(f'{task_dict[i][0]}, {task_dict[i][1]}, {task_dict[i][2]}, {task_dict[i][3]}, {task_dict[i][4]},'
                    f' {task_dict[i][5]}\n')

    # Update report files
    generate_reports()
    return


# Printout the summary of tasks and users
def view_stats():

    # Loop to generate stats file in case one does not exist
    while True:
        try:

            # Open and print the task and user summary files
            with open('user_overview.txt', 'r') as f:
                print(f.read())
            print('')
            with open('task_overview.txt', 'r') as f:
                print(f.read())
            break

        # In case of no file, run the 'generate stats' function
        except FileNotFoundError:
            generate_reports()


# Create a dictionary of the current logged tasks, used for easier coding operations
def create_task_dictionary():

    # Open tasks file, create a list of all tasks
    with open("tasks.txt", 'r') as f:
        all_tasks = []
        task_lines = f.read().splitlines()

    # Iterate through all tasks and separate tasks information into a sub-list (task details)
    for values in task_lines:
        task_details = values.split(', ')
        all_tasks.append(task_details)

    # Create dictionary from all tasks list
    task_dict = dict((key, value) for key, value in enumerate(all_tasks))

    return task_dict


# Generate the summary of the users and the tasks
def generate_reports():

    # Open the task database and create dictionary, initialise counters
    task_dict = create_task_dictionary()
    user_dict = create_user_dictionary()
    tasks_complete = 0
    tasks_incomplete = 0
    tasks_overdue = 0

    # Calculate report values, complete/incomplete/overdue
    for id, tasks in task_dict.items():
        if tasks[5].lower() == 'yes':
            tasks_complete += 1
        else:
            tasks_incomplete += 1
            if datetime.strptime(tasks[4], "%d %b %Y").date() < date.today():
                tasks_overdue += 1

    # Calculate report values, total/percentages
    total_tasks = len(task_dict)
    percent_incomplete = round(100 * (tasks_incomplete / total_tasks))
    percent_overdue = round(100 * (tasks_overdue / total_tasks))

    # Write the task summary to file
    with open('user_overview.txt', 'w+') as f:
        f.write(
            f'Total tasks:\t\t{total_tasks}\nTasks complete:\t\t{tasks_complete}\nTasks incomplete:\t{tasks_incomplete}\n'
            f'Tasks overdue:\t\t{tasks_overdue}\n% incomplete:\t\t{percent_incomplete}\n% overdue:\t\t\t{percent_overdue}')

    # Write header for user summary to file
    with open('task_overview.txt', 'w+') as f:
        f.write(f'user\t%total\t%complete\t%incomplete\t%overdue\n'
                f'------------------------------------------------')

    # Calculate the user data, iterate through each name in user database
    for user in user_dict:

        # Reset counters
        task_of_user = 0
        tasks_complete = 0
        tasks_incomplete = 0
        tasks_overdue = 0

        # Iterate through tasks, pick out tasks matching said user, count complete/incomplete/overdue tasks
        for id, tasks in task_dict.items():
            if user == task_dict[id][0]:
                task_of_user += 1
                if tasks[5].lower() == 'yes':
                    tasks_complete += 1
                else:
                    tasks_incomplete += 1
                    if datetime.strptime(tasks[4], "%d %b %Y").date() < date.today():
                        tasks_overdue += 1

        # Using the counts, calculate tasks statistics for said user
        percentage_of_total = int(100 * (task_of_user / total_tasks))
        if task_of_user == 0:
            percentage_complete = 'N/A'
            percentage_incomplete = 'N/A'
            percentage_overdue = 'N/A'
        else:
            percentage_incomplete = int(100 * (tasks_incomplete / task_of_user))
            percentage_overdue = int(100 * (tasks_overdue / task_of_user))
            percentage_complete = int(100 * (tasks_complete / task_of_user))

        # Write the calculated statistics to file
        with open('task_overview.txt', 'a') as f:
            f.write(
            f'\n{user}:\t{percentage_of_total}\t\t{percentage_complete}\t\t\t{percentage_incomplete}'
            f'\t\t\t{percentage_overdue}')


# Create a dictionary of the current user data base, used for easier coding operations
def create_user_dictionary():

    # Open tasks file, create a list of all tasks
    with open("tasks.txt", 'r') as f:
        all_tasks = []
        task_lines = f.read().splitlines()

    # Iterate through all tasks and separate tasks information into a sub-list (task details)
    for values in task_lines:
        task_details = values.split(', ')
        all_tasks.append(task_details)

    # Create dictionary from all tasks list
    user_dict = {names[i]: passwords[i] for i in range(len(names))}

    return user_dict


# Print task information for given task number
def print_tasks(dictionary, key):
    print(f'''------------------------------------------------------
    Task:\t\t\t\t{dictionary[key][1]}
    Assigned to:\t\t{dictionary[key][0]}
    Date assigned:\t\t{dictionary[key][3]}
    Due date:\t\t\t{dictionary[key][4]}
    Task complete?:\t\t{dictionary[key][5]}
    Task description:\t{dictionary[key][2]}
    ------------------------------------------------------''')


#================Login Section================

# Open user info file and populate lists of names and passwords
with open('user.txt', 'r') as f:

    # Initialise user info lists
    names = []
    passwords = []

    # Divide info in the lines of input file to populate user info lists
    user_lines = f.read().splitlines()
    for entry in user_lines:
        names.append(entry.split(', ')[0])
        passwords.append(entry.split(', ')[1])

# Loop to ensure correct username entered
while True:

    username_input = input("Enter username (case sensitive): ")
    if username_input in names:
        break
    else:
        print("Username not found")
        continue

# Loop to ensure correct password entered
while True:

    password_input = input("Enter password (case sensitive): ")
    if password_input in passwords:
        print("Welcome")
        break
    else:
        print("Password incorrect")
        continue
    break

# ================MAIN================

while True:

    if username_input == 'admin':
        # For admin, presenting the menu to the user and making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
        r - Registering a user
        a - Adding a task
        va - View all tasks
        vm - View my task
        gr - Generate reports
        s - View statistics
        e - Exit
        : ''').lower()
    else:
        # For normal user, presenting the menu to the user and making sure that the user input is converted to lower case.
        menu = input('''Select one of the following Options below:
        a - Adding a task
        va - View all tasks
        vm - View my task
        e - Exit
        : ''').lower()

    if menu == 'r' and username_input == 'admin': # Add new user information, admin only
        reg_user_admin(names)
    elif menu == 'a': # Add new task
        add_task()
    elif menu == 'va': # Printout all tasks
        view_all()
    elif menu == 'vm': # Print out tasks of specific user
        view_mine(username_input)
    elif menu == 'gr':  # Create text files of tasks and users
        generate_reports()
    elif menu == 's': # Print statistics for task and user databases
        view_stats()
    elif menu == 'e': # Exit program
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please try again\n")