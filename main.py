import sqlite3 as sql


def create_tables(cursor):
    # Create the tables if necessary

    cursor.execute("CREATE TABLE IF NOT EXISTS Pupil (PupilID INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT);")

    cursor.execute("CREATE TABLE IF NOT EXISTS Subject (SubjectID INTEGER PRIMARY KEY, SubjectName TEXT);")

    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS PupilSubjects (
        PupilSubjectID INTEGER PRIMARY KEY,
        PupilID INTEGER,
        SubjectID INTEGER
        );''')

    print('Created the tables, if necessary')


# Functions to add and query pupils

def add_pupil(cursor, FirstName, LastName):
    pupil_insert_cmd = "INSERT INTO Pupil (FirstName, LastName) VALUES (?, ?);"

    cursor.execute(pupil_insert_cmd, (FirstName, LastName))

    return get_PupilID(cursor, FirstName, LastName)


def get_pupil(cursor, FirstName, LastName):
    pupil_existence_cmd = "SELECT * FROM Pupil WHERE FirstName=? AND LastName=?;"

    cursor.execute(pupil_existence_cmd, (FirstName, LastName))
    return cursor.fetchone()


def get_PupilID(cursor, FirstName, LastName):
    pupilID_existence_cmd = "SELECT PupilID FROM Pupil WHERE FirstName=? AND LastName=?;"

    cursor.execute(pupilID_existence_cmd, (FirstName, LastName))

    fetch = cursor.fetchone()

    if fetch:
        PupilID, = fetch
    else:
        PupilID = None
    return PupilID


def get_all_pupils(cursor):
    pupil_get_cmd = "SELECT * FROM Pupil;"

    cursor.execute(pupil_get_cmd)
    return cursor.fetchall()


# Functions to add and query pupils

def add_subject(cursor, SubjectName):
    subject_insert_cmd = "INSERT INTO Subject (SubjectName) VALUES (?);"

    cursor.execute(subject_insert_cmd, (SubjectName,))

    return get_SubjectID(cursor, SubjectName)


def get_subject(cursor, SubjectName):
    subject_existence_cmd = "SELECT * FROM Subject WHERE SubjectName=?;"

    cursor.execute(subject_existence_cmd, (SubjectName,))
    return cursor.fetchone()


def get_SubjectID(cursor, SubjectName):
    subjectID_existence_cmd = "SELECT SubjectID FROM Subject WHERE SubjectName=?;"

    cursor.execute(subjectID_existence_cmd, (SubjectName,))
    fetch = cursor.fetchone()

    if fetch:
        subject_id, = fetch
    else:
        subject_id = None
    return subject_id


def get_all_subjects(cursor):
    subject_get_cmd = "SELECT * FROM Subject;"

    cursor.execute(subject_get_cmd)
    return cursor.fetchall()


# Manage pupil subjects

def add_pupil_subject(cursor, PupilID, SubjectID):
    add_pupil_subject_cmd = 'INSERT INTO PupilSubjects (PupilID, SubjectID) VALUES (?, ?);'

    cursor.execute(add_pupil_subject_cmd, (PupilID, SubjectID))

    return get_pupil_subject_id(cursor, PupilID, SubjectID)


def get_pupil_subject_id(cursor, PupilID, SubjectID):
    pupil_subject_id_existence_cmd = "SELECT PupilSubjectID FROM PupilSubjects WHERE PupilID=? AND SubjectID=?;"

    cursor.execute(pupil_subject_id_existence_cmd, (PupilID, SubjectID))

    fetch = cursor.fetchone()

    if fetch:
        PupilSubjectID, = fetch
    else:
        PupilSubjectID = None
    return PupilSubjectID


# The magic bit - we'll use a JOIN to get a report

def get_all_pupil_subjects(cursor):
    pupil_subjects_cmd = '''SELECT LastName, FirstName, SubjectName
                            FROM Pupil
                            JOIN Subject
                            JOIN PupilSubjects
                            ON Pupil.PupilID=PupilSubjects.PupilID
                            AND Subject.SubjectID=PupilSubjects.SubjectID;'''

    cursor.execute(pupil_subjects_cmd)
    return cursor.fetchall()


# Create our connection. This needs doing properly.

if __name__ == '__main__':
    with sql.connect('my.db') as conn:
        cursor = conn.cursor()

        # Create our tables if necessary

        create_tables(cursor)

        BobID = get_PupilID(cursor, 'Bob', 'Smith')

        if not BobID:
            BobID = add_pupil(cursor, 'Bob', 'Smith')

        MathID = get_SubjectID(cursor, 'Mathematics')

        if not MathID:
            MathID = add_subject(cursor, 'Mathematics')

        if not get_pupil_subject_id(cursor, BobID, MathID):
            add_pupil_subject(cursor, BobID, MathID)

        conn.commit()

        while True:
            for (LastName, FirstName, SubjectName) in get_all_pupil_subjects(cursor):
                print(f'{FirstName} {LastName} - {SubjectName}')

            print('1 - Add Pupil\n2 - Add Subject\n3 - Add combination')

            choice = None

            while not choice:
                choice_entry = input('Make a choice:')

                if choice_entry == '1':
                    choice = 1
                elif choice_entry == '2':
                    choice = 2
                elif choice_entry == '3':
                    choice = 3

            if choice == 1:
                last_name = input('Last name: ')
                first_name = input('First name: ')

                pupil_id = get_PupilID(cursor, first_name, last_name)

                if pupil_id:
                    print('Pupil already in database')
                else:
                    add_pupil(cursor, first_name, last_name)

            if choice == 2:
                subject_name = input('Subject name: ')

                subject_id = get_SubjectID(cursor, subject_name)

                if subject_id:
                    print('Subject already in database')
                else:
                    add_subject(cursor, subject_name)

            if choice == 3:
                pupil_id = None

                while not pupil_id:
                    last_name = input('Last name: ')
                    first_name = input('First name: ')

                    pupil_id = get_PupilID(cursor, first_name, last_name)

                subject_id = None

                while not subject_id:
                    subject_name = input('Subject name: ')

                    subject_id = get_SubjectID(cursor, subject_name)

                pupil_subject_id = get_pupil_subject_id(cursor, pupil_id, subject_id)

                if pupil_subject_id:
                    print('Combination already in database')
                else:
                    add_pupil_subject(cursor, pupil_id, subject_id)


