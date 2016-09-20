import unittest.mock
import unittest

import main
import models
import validations


class ValidationsTest(unittest.TestCase):
    def setUp(self):
        self.good_date = '26/04/1980'
        self.good_date2 = '26/05/1980'
        self.bad_date = '26041980'
        self.good_time = '2'
        self.bad_time = ''

    def test_good_date_validation(self):
        good_date_result = validations.check_date(self.good_date)
        self.assertIsInstance(good_date_result, models.datetime.datetime)

    def test_bad_date_validation(self):
        bad_date_result = validations.check_date(self.bad_date)
        self.assertIsInstance(bad_date_result, str)

    def test_bad_time_validation(self):
        bad_time_result = validations.check_time(self.bad_time)
        self.assertIsInstance(bad_time_result, str)

    def test_good_time_validation(self):
        good_time_result = validations.check_time(self.good_time)
        self.assertIsInstance(good_time_result, int)

    def test_good_dates_validation(self):
        good_dates_result = validations.check_dates(self.good_date2, self.good_date)
        self.assertIsInstance(good_dates_result, tuple)
        d1, d2 = good_dates_result
        self.assertGreaterEqual(d2, d1)
        good_dates_result = validations.check_dates(self.good_date, self.good_date2)
        self.assertIsInstance(good_dates_result, tuple)
        d1, d2 = good_dates_result
        self.assertLessEqual(d1, d2)

    def test_very_bad_dates_validation(self):
        very_bad_dates = validations.check_dates(self.bad_date, self.good_time)
        self.assertIsInstance(very_bad_dates, list)
        msg1, msg2 = very_bad_dates
        self.assertIsInstance(msg1, str)
        self.assertIsInstance(msg2, str)

    def test_slightly_bad_dates_validation(self):
        badish_dates = validations.check_dates(self.good_date, self.bad_date)
        d3, d4 = badish_dates
        self.assertIsInstance(d3, models.datetime.datetime)
        self.assertIsInstance(d4, str)
        badish_dates = validations.check_dates(self.bad_date, self.good_date)
        d5, d6 = badish_dates
        self.assertIsInstance(d6, models.datetime.datetime)
        self.assertIsInstance(d5, str)


class ModelsEntryTest(unittest.TestCase):
    def setUp(self):
        self.employee = 'Test Employee'
        self.date = models.datetime.datetime(day=25, month=5, year=2011)
        self.job = 'Test Job'
        self.time = 20
        self.notes = 'Test Notes'

    def test_entry_creation_and_deletion(self):
        models.Entry.add_entry(
            emp=self.employee,
            date=self.date,
            job=self.job,
            minutes=self.time,
            notes=self.notes
        )
        with self.assertRaises(ValueError):
            models.Entry.add_entry(
                emp=self.employee,
                date=self.date,
                job=self.job,
                minutes=self.time,
                notes=self.notes
            )
        retrieve_entry = models.Entry.get_entry(
            emp=self.employee,
            date=self.date,
            job=self.job,
            minutes=self.time,
            notes=self.notes
        )
        self.assertIsInstance(retrieve_entry, models.Entry)
        e_string = retrieve_entry.__str__()
        self.assertIsInstance(e_string, str)
        deletion = models.Entry.delete().where(models.Entry.entry_job == 'Test Job')
        deletion.execute()
        with self.assertRaises(models.DoesNotExist):
            zero_entry = models.Entry.get_entry(
                emp=self.employee,
                date=self.date,
                job=self.job,
                minutes=self.time,
                notes=self.notes
            )


class ModelsProjectTest(unittest.TestCase):
    def setUp(self):
        self.project_title = 'No Project'
        self.start_time = models.datetime.datetime(day=3, month=3, year=2003)

    def test_project_operations(self):
        deletion = models.Project.delete().where((models.Project.project_name == 'No Project') &
                                                 (models.Project.start_date == self.start_time))
        deletion.execute()
        models.Project.add_project(self.project_title, self.start_time)
        project_ret = models.Project.select().where(
            models.Project.project_name == self.project_title).get()
        self.assertIsInstance(project_ret, models.Project)
        with self.assertRaises(ValueError):
            models.Project.add_project(
                self.project_title, self.start_time
            )
        p_string = project_ret.__str__()
        self.assertEqual(p_string, 'No Project: started on 03/03/2003')
        models.Project.delete_instance(project_ret)
        with self.assertRaises(models.DoesNotExist):
            models.Project.get(models.Project.project_name == self.project_title,
                                         models.Project.start_date == self.start_time)


class MainTest(unittest.TestCase):

    def test_make_notes_mocking(self):
        with unittest.mock.patch('builtins.input', return_value='Here are the notes'):
            self.assertIs(main.make_notes(), 'Here are the notes')

    @unittest.mock.patch('main.quit_program')
    @unittest.mock.patch('main.main_menu')
    def test_main_menu_calls_add_project(self, mock_main_menu, mock_quit_program):
        with unittest.mock.patch('builtins.input', return_value='q'):
            mock_main_menu.start()
            self.assertTrue(mock_quit_program.called_with())

    @unittest.mock.patch('main.add_project')
    @unittest.mock.patch('main.main_menu')
    def test_main_menu_calls_add_project(self, mock_main_menu, mock_add_project):
        with unittest.mock.patch('builtins.input', return_value='p'):
            mock_main_menu.start()
            self.assertTrue(mock_add_project.called_with())

    @unittest.mock.patch('main.search_entry')
    @unittest.mock.patch('main.main_menu')
    def test_main_menu_calls_add_project(self, mock_main_menu, mock_search_entry):
        with unittest.mock.patch('builtins.input', return_value='s'):
            mock_main_menu.start()
            self.assertTrue(mock_search_entry.called_with())

    @unittest.mock.patch('main.view_entries')
    @unittest.mock.patch('main.main_menu')
    def test_main_menu_calls_add_project(self, mock_main_menu, mock_view_entries):
        with unittest.mock.patch('builtins.input', return_value='r'):
            mock_main_menu.start()
            self.assertTrue(mock_view_entries.called_with())

if __name__ == '__main__':
    unittest.main()