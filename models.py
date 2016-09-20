import datetime

from peewee import *

from config import CONFIG


database = SqliteDatabase(CONFIG['database_name'])


class BaseModel(Model):

    class Meta:
        database = database


class Project(BaseModel):
    project_name = CharField(max_length=100)
    start_date = DateTimeField(default=datetime.datetime.now)
    completed = BooleanField()

    def __str__(self):
        return '{0}: started on {1}'.format(
            self.project_name,
            datetime.datetime.strftime(self.start_date, CONFIG['date_string_format'])
        )

    @classmethod
    def add_project(cls, name, start, completed=False):
        try:
            cls.get(
                cls.project_name == name,
                cls.start_date == start
            )
        except DoesNotExist:
            cls.create(
                project_name=name,
                start_date=start,
                completed=completed
            )
        else:
            raise ValueError('A project with that name and start date already exists')

    @classmethod
    def get_projects(cls):
        return cls.select().order_by(cls.start_date).order_by(cls.id)

    @classmethod
    def find_all_entries_for_project(cls, pk):
        project = cls.get(cls.id == pk)
        return Entry.select().join(JobForProject, on=JobForProject.job_done).where(
            JobForProject.project_for == project)


class Entry(BaseModel):
    entry_employee = CharField(max_length=100, default='No Employee Name')
    entry_date = DateTimeField(default=datetime.datetime.now)
    entry_job = CharField(default='Unspecified', max_length=150)
    entry_time = IntegerField(default=0)
    entry_notes = TextField(default='No notes Recorded')

    def __str__(self):
        try:
            entry_project = self.get_entry_project()
        except DoesNotExist:
            return 'Date: {1}\nEmployee: {0.entry_employee}\nJob: {0.entry_job}\n' \
                   'Minutes Spent: {0.entry_time}\nNotes: {0.entry_notes}\n' \
                   'Project: None'.format(self,
                                          datetime.datetime.strftime(
                                              self.entry_date,
                                              CONFIG['date_string_format']
                                            )
                                          )
        else:
            return 'Date: {2}\nEmployee: {0.entry_employee}\nJob: {0.entry_job}\n' \
                   'Minutes Spent: {0.entry_time}\nNotes: {0.entry_notes}\n' \
                   'Project: {1.project_name}'.format(
                                                self,
                                                entry_project,
                                                datetime.datetime.strftime(
                                                    self.entry_date,
                                                    CONFIG['date_string_format']
                                                    )
                                                )

    def get_entry_project(self):
        return Project.select().join(JobForProject, on=JobForProject.project_for).where(
                JobForProject.job_done == self).get()

    @classmethod
    def all_entries(cls):
        return cls.select().order_by(cls.entry_date)

    @classmethod
    def get_entry(cls, emp, date, job, minutes, notes):
        return cls.get(
            entry_employee=emp,
            entry_date=date,
            entry_job=job,
            entry_time=minutes,
            entry_notes=notes
        )

    @classmethod
    def add_entry(cls, emp, date, job, minutes, notes):
        try:
            cls.get(
                cls.entry_employee == emp,
                cls.entry_date == date,
                cls.entry_job == job,
                cls.entry_time == minutes,
                cls.entry_notes == notes
                )
        except DoesNotExist:
            cls.create(
                entry_employee=emp,
                entry_date=date,
                entry_job=job,
                entry_time=minutes,
                entry_notes=notes
            )
        else:
            raise ValueError("That exact entry already exists")

    @classmethod
    def build_date_range_query(cls, date_tuple):
        return cls.select().where((cls.entry_date >= date_tuple[0]) & (cls.entry_date <= date_tuple[1])
                                  ).order_by(cls.entry_date.desc())

    @classmethod
    def build_string_query(cls, string):
        return [entry for entry in cls.select()
                if string in entry.entry_job or string in entry.entry_notes]

    @classmethod
    def build_single_date_query(cls, date1):
        return cls.select().where(cls.entry_date == date1)

    @classmethod
    def build_time_query(cls, time1, time2=None):
        if time2:
            return cls.select().where((cls.entry_time >= time1) & (cls.entry_time <= time2))
        else:
            return cls.select().where(cls.entry_time == time1)

    @classmethod
    def build_employees(cls, string):
        employee_names = set()
        for emp in cls.select():
            for nom in emp.entry_employee.lower().split():
                if nom in string.split():
                    employee_names.add(emp.entry_employee)
        return employee_names

    @classmethod
    def get_employee_entries(cls, emp_name):
        return cls.select().where(cls.entry_employee == emp_name)


class JobForProject(BaseModel):
    job_done = ForeignKeyField(rel_model=Entry, related_name='project_for')
    project_for = ForeignKeyField(rel_model=Project, related_name='jobs')

    class Meta:
        indexes = (
            (('job_done', 'project_for'), True),
        )

    @classmethod
    def link_job_to_project(cls, job_obj, project_obj):
        cls.create(
            job_done=job_obj,
            project_for=project_obj
        )

    @classmethod
    def remove_project_association(cls, e_1, p_1):
        deletion = cls.delete().where((JobForProject.job_done == e_1) &
                           (JobForProject.project_for == p_1))
        deletion.execute()