import os
import sys
from numpy import genfromtxt

files = []

path_files = ""


def open_files():
    global path_files

    path_files = sys.argv[1] + '\\'

    list_files = [f for f in os.listdir(path_files)]

    if len(list_files) < 2:
        raise ValueError(
            'should be only one 9A or 2A file in the current directory')

    global files
    files = list(filter(lambda x: x.endswith("2A")
                        or x.endswith("9A"), list_files))


def calculate(file_two, file_nine):
    my_data = genfromtxt(path_files + file_two, usecols=(8, 9),
                         dtype=None, delimiter=',', skip_header=1)

    count_two = 0
    for row in my_data:
        if row[0] != 0 and row[1] != 0:
            count_two += (row[1] - row[0]) + 1

    header_nine = ''
    with open(path_files + file_nine, 'r') as f:
        header_nine = f.readline()

    result = "Turno " + file_two[-3] + ": " + \
        str(int(header_nine[-6:]) - count_two)

    return result


if __name__ == '__main__':
    try:
        open_files()
        if len(files):
            files_4 = list(filter(lambda x: x.endswith('42A')
                                  or x.endswith('49A'), files))

            files_5 = list(filter(lambda x: x.endswith('52A')
                                  or x.endswith('59A'), files))

            files_6 = list(filter(lambda x: x.endswith('62A')
                                  or x.endswith('69A'), files))

            if len(files_4):
                print(calculate(next((f for f in files_4 if f.endswith('2A')), None),
                                next((f for f in files_4 if f.endswith('9A')), None)))

            if len(files_5):
                print(calculate(next((f for f in files_5 if f.endswith('2A')), None),
                                next((f for f in files_5 if f.endswith('9A')), None)))

            if len(files_6):
                print(calculate(next((f for f in files_6 if f.endswith('2A')), None),
                                next((f for f in files_6 if f.endswith('9A')), None)))
    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("\nPress Enter to continue ...")
        input()
