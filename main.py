#!/usr/bin/env/python3

import os
import sys
import time
import validations

from config import CONFIG
import models


def clear_screen():
    """Clears the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def quit_program():
    """exits the program"""
    models.database.close()
    sys.exit()


def menu_print(menu_dict):
    """Prints the formatted menu to screen from an ordered dict passed as an parameter"""
    for key, value in menu_dict.items():
        print(key + ': ' + value)
    print()


def make_notes():
    """Prompts the user to input text, with input() or sys.stdin.read()
    depending on OS, returns the text"""
    message = "Please enter your notes for this task."
    if os.name == 'nt':
        print(message + ' press return/enter when finished.')
        notes = input('> ').strip()
    else:
        print(message + ' Enter ctrl-d when finished')
        notes = sys.stdin.read().strip()
    return notes


def associate_project(entry_to_link):
    clear_screen()
    while True:
        for project in models.Project.get_projects():
            print(project)
            yes_no = input("Associate with this project? [y/n] or 'q' to quit ").lower().strip()
            if yes_no == 'y':
                models.JobForProject.link_job_to_project(entry_to_link, project)
                print("Done")
                time.sleep(2)
                main_menu()
            elif yes_no == 'n':
                continue
            elif yes_no == 'q':
                break


def add_entry():
    clear_screen()
    print("Go ahead and create your entry\n")
    emp = input("Enter the employees name > ").strip()
    while True:
        date = validations.check_date(input("Enter entry date as dd/mm/yyy > "))
        if isinstance(date, models.datetime.datetime):
            break
        else:
            print(date)
            continue
    job = input("Enter the entry job > ")
    while True:
        minutes = validations.check_time(input("Enter the time spent as a number > "))
        if isinstance(minutes, int):
            break
        else:
            print(minutes)
            continue
    notes = make_notes()
    models.Entry.add_entry(emp, date, job, minutes, notes)
    if models.Project.get_projects():
        assoc = input("Do you want to associate this entry with a project? [y/n] > ").lower().strip()
        if assoc == 'y':
            entry_to_assoc = models.Entry.get_entry(emp, date, job, minutes, notes)
            associate_project(entry_to_assoc)


def add_project():
    clear_screen()
    print("Go ahead and add a project\n")
    pname = input("Enter the project name > ")
    while True:
        pstart = validations.check_date(input("Enter the start date as dd/mm/yyyy > "))
        if isinstance(pstart, models.datetime.datetime):
            break
        else:
            print(pstart)
            continue
    models.Project.add_project(pname, pstart)


def view_projects():
    clear_screen()
    projects = models.Project.get_projects()
    if projects:
        print("Here are all the projects\n")
        for project in projects:
            print('{}, {}'.format(project.id, project))
        print()
        see = input("Do you want to see the entries associated with a project?"
                    "\nenter the number next to the project if you do\nif you enter anything other than a number"
                    " next to a project you will return to the main menu if not a number\nor see no entries returned"
                    "if the number was not next to a project > ")
        if isinstance(validations.check_time(see), int):
            p_ents = models.Project.find_all_entries_for_project(see)
            if p_ents:
                view_entries(p_ents)
            else:
                print('No entries to show yet')
                time.sleep(2)
                main_menu()
        else:
            main_menu()
    else:
        print("No projects at present")
    input("\nPress any key to go back to the main menu")


def edit_entry(entry):
    clear_screen()
    while True:
        print("Edit entry\n")
        print(entry)
        print()
        menu_print(CONFIG['edit_menu'])
        edit_choice = input("What do you want to do? > ")
        if edit_choice == 'q':
            break
        elif edit_choice == 'd':
            new_date = validations.check_date(input("enter new date as dd/mm/yyyy > "))
            if isinstance(new_date, models.datetime.datetime):
                entry.entry_date = new_date
                entry.save()
                print("Date updated")
            else:
                print(new_date)
        elif edit_choice == 't':
            new_time = validations.check_time(input("Enter the new number of minutes"))
            if isinstance(new_time, int):
                entry.entry_time = new_time
                entry.save()
                print("Minutes spent updated")
            else:
                print(new_time)
        elif edit_choice == 'e':
            new_emp = input("Enter new employee name > ").strip()
            entry.entry_employee = new_emp
            entry.save()
            print("Employee name updated")
        elif edit_choice == 'j':
            new_job = input("Enter new job title > ")
            entry.entry_job = new_job
            entry.save()
            print("Job updated")
        elif edit_choice == 'n':
            new_notes = make_notes()
            entry.entry_notes = new_notes
            entry.save()
            print("Notes updated")
        elif edit_choice == 'p':
            try:
                entry_project = entry.get_entry_project()
            except models.DoesNotExist:
                associate_project(entry)
            else:
                delete_or_change = input("Do you want to set this entries project to none 'n' "
                                        "or associate with another project ('a') or leave it as it is ('l') > ")
                if delete_or_change == 'l':
                    continue
                elif delete_or_change == 'n':
                    models.JobForProject.remove_project_association(entry, entry_project)
                elif delete_or_change == 'a':
                    models.JobForProject.remove_project_association(entry, entry_project)
                    associate_project(entry)
        else:
            print("That was not understood, try again")
            continue
        time.sleep(2)


def view_entries(query_obj):
    counter = 0
    entries = query_obj
    if entries:
        while True:
            last_entry = len(entries)
            clear_screen()
            print("Entry {} of {}".format(counter + 1, last_entry))
            print(entries[counter])
            print()
            menu_print(CONFIG['task_menu'])
            selection = input("What do you want to do? > ")
            if selection == 'r':
                main_menu()
            elif selection == 'n':
                if counter == last_entry - 1:
                    counter = 0
                    continue
                else:
                    counter += 1
                    continue
            elif selection == 'b':
                if counter == 0:
                    counter = last_entry - 1
                    continue
                else:
                    counter -= 1
                    continue
            elif selection == 'e':
                edit_entry(entries[counter])
            elif selection == 'd':
                models.Entry.delete_instance(entries[counter])
                search_entry()
            else:
                print("That was not recognised, try again")
                continue
    else:
        clear_screen()
        print("No entries found")
        input("\npress any key to continue")
        search_entry()


def date_search():
    while True:
        clear_screen()
        howto = input("Search by a specific date ('s') or a range of dates ('r') > ").lower().strip()
        if howto == 's':
            while True:
                d1 = validations.check_date(input("Enter the date as dd/mm/yyyy > "))
                if isinstance(d1, models.datetime.datetime):
                    view_entries(models.Entry.build_single_date_query(d1))
                else:
                    print("date must be entered as dd/mm/yyyy")
        elif howto == 'r':
            while True:
                d2 = input("Enter the start date as dd/mm/yyyy > ")
                d3 = input("Enter the end date as dd/mm/yyyy > ")
                returns = validations.check_dates(d2, d3)
                if isinstance(returns, tuple):
                    view_entries(models.Entry.build_date_range_query(returns))
                else:
                    if isinstance(returns[0], str) and isinstance(returns[1], str):
                        print(*returns)
                    elif isinstance(returns[0], str):
                        print(returns[0])
                    else:
                        print(returns[1])
        else:
            print("sorry that was not recognised")
            time.sleep(2)


def time_search():
    while True:
        clear_screen()
        howtime = input("Search for a specific time ('s') or a range of times('r') > ").lower().strip()
        if howtime == 's':
            while True:
                t1 = validations.check_time(input("Enter the time as a number > "))
                if isinstance(t1, int):
                    view_entries(models.Entry.build_time_query(t1))
                else:
                    print(t1)
        elif howtime == 'r':
            while True:
                t2 = validations.check_time(input("Enter the lower time to search between"))
                if isinstance(t2, int):
                    break
                else:
                    print(t2)
            while True:
                t3 = validations.check_time(input("Enter the lower time to search between"))
                if isinstance(t3, int):
                    break
                else:
                    print(t3)
            view_entries(models.Entry.build_time_query(t2, t3))


def string_search():
    clear_screen()
    string_to_search = input("Enter the text you want to search for > ")
    view_entries(models.Entry.build_string_query(string_to_search))


def dates_with_entries():
    clear_screen()
    entry_dict = {}
    for entry in models.Entry.select():
        try:
            entry_dict[models.datetime.datetime.strftime(
                entry.entry_date, CONFIG['date_string_format']
            )]
        except KeyError:
            entry_dict[models.datetime.datetime.strftime(
                entry.entry_date, CONFIG['date_string_format']
            )] = 1
        else:
            entry_dict[models.datetime.datetime.strftime(
                entry.entry_date, CONFIG['date_string_format']
            )] += 1
    for key, value in entry_dict.items():
        print('{}, {}'.format(key, value))
    while True:
        see_e = validations.check_date(input("Enter the date you want to see entries for as dd/mm/yyy > "))
        if isinstance(see_e, models.datetime.datetime):
            view_entries(models.Entry.build_single_date_query(see_e))
        else:
            print(see_e)


def employee_search():
    clear_screen()
    employee = input("Enter the employee name to search for > ").lower().strip()
    employees = models.Entry.build_employees(employee)
    employee_display = [(i, name) for i, name in enumerate(employees)]
    if employee_display:
        print("\nHere are the employees that match that with entries")
        print()
        for index, nom in employee_display:
            print("{}: {}".format(index, nom))
        print()
        employee_display = dict(employee_display)
        while True:
            e_choice = validations.check_time(
                input("Enter the number next to the name you want to see entries for > ")
            )
            if isinstance(e_choice, int):
                try:
                    e1 = employee_display[e_choice]
                except KeyError:
                    print("That was not a number next to a name, try again")
                    continue
                else:
                    view_entries(models.Entry.get_employee_entries(e1))
            else:
                print("That was not a number...")
                continue
    else:
        print("Nothing found for that input")
        time.sleep(2)
        search_entry()


def search_entry():
    while True:
        clear_screen()
        menu_print(CONFIG['search_menu'])
        search_method = input("How do you want to search? ")
        if search_method == 'v':
            dates_with_entries()
        elif search_method == 'd':
            date_search()
        elif search_method == 'e':
            employee_search()
        elif search_method == 't':
            time_search()
        elif search_method == 's':
            string_search()
        elif search_method == 'z':
            main_menu()
        else:
            print("That was not recognised, please try again")
            time.sleep(2)
            continue


def main_menu():
    while True:
        clear_screen()
        print("You are using the work logger 2.1\n")
        menu_print(CONFIG['main_menu'])
        main_choice = input("what do you want to do > ")
        if main_choice == 'a':
            add_entry()
        elif main_choice == 's':
            search_entry()
        elif main_choice == 'p':
            add_project()
        elif main_choice == 'l':
            view_projects()
        elif main_choice == 'r':
            view_entries(models.Entry.all_entries())
        elif main_choice == 'q':
            quit_program()
        else:
            clear_screen()
            print("That was not recognised please try again...")
            time.sleep(2)
            continue


def initialize_database():
    """connects to the database and creates tables under safe mode"""
    models.database.connect()
    models.database.create_tables([models.Entry, models.Project, models.JobForProject], safe=True)


if __name__ == '__main__':

    initialize_database()
    main_menu()