from collections import OrderedDict

CONFIG = {
    'database_name': 'work_log_database.db',
    'date_string_format': '%d/%m/%Y',
    'date_check_failure_msg': 'date entry must be in the form dd/mm/yyy\n'
                          'for example 6th June 1944 should be entered 06/06/1944',
    'time_check_failure_msg': 'You must enter the minutes spent on the task as a number\n'
                              'use 0-9 only, no letters or anything else',
    'main_menu': OrderedDict([
                    ('a', 'add task'),
                    ('s', 'search tasks'),
                    ('p', 'add project'),
                    ('l', 'show projects'),
                    ('r', 'see all entries'),
                    ('q', 'Quit'),
                    ]),
    'task_menu': OrderedDict([
                    ('n', 'See next task'),
                    ('b', 'Go back to previous task'),
                    ('e', 'Edit this task'),
                    ('d', 'Delete this task'),
                    ('r', 'Back to main menu'),
                    ]),
    'edit_menu': OrderedDict([
                    ('d', 'Change date'),
                    ('t', 'Change time spent'),
                    ('e', 'Change employee name'),
                    ('j', 'Change job name'),
                    ('n', 'Change notes'),
                    ('q', 'go back'),
                    ('p', 'Change project'),
                    ]),
    'search_menu': OrderedDict([
                    ('v', 'See dates with entries'),
                    ('d', 'Search entries by date'),
                    ('e', 'Search by employee name'),
                    ('t', 'Search by time spent'),
                    ('s', 'Search by text'),
                    ('z', 'Return to the main menu'),
                    ]),
}