import os
import sys
from numpy import genfromtxt

files = []

path_files = ""


def open_files():
    global path_files

    path_files = "/home/geezylucas/Documentos/Python3/floorfiles/"
    # path_files = sys.argv[1] + '\\'

    list_files = [f for f in os.listdir(path_files)]

    if len(list_files) < 2:
        raise ValueError(
            'should be only one 9A or 2A file in the current directory')

    global files
    files = list(filter(lambda x: x.endswith("2A")
                        or x.endswith("9A"), list_files))


def calculate(file_two, file_nine):
    my_data = genfromtxt(path_files + file_two, usecols=(4, 5, 6, 8, 9),
                         dtype=None, delimiter=',', skip_header=1)

    list_diff_ocu = []
    count_two = 0
    for row in my_data:
        if row[3] != 0 and row[4] != 0:
            count_occurrences = (row[4] - row[3]) + 1
            count_two += count_occurrences

            text_to_search = f"{row[0]},{row[1]},{(row[2].decode('utf-8'))}"
            occurrences_found = int(
                open(path_files + file_nine, 'r').read().count(text_to_search))

            difference = occurrences_found - count_occurrences

            if difference != 0:
                list_diff_ocu.append(text_to_search + ": " + str(difference))

    header_nine = ''
    with open(path_files + file_nine, 'r') as f:
        header_nine = f.readline()

    result = "Turno " + file_two[-3] + ": " + \
        str(int(header_nine[-6:]) - count_two)

    return result, list_diff_ocu


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
                result, list_diff = calculate(next((f for f in files_4 if f.endswith('2A')), None),
                                              next((f for f in files_4 if f.endswith('9A')), None))

                print(result)
                if result != 0:
                    for p in list_diff:
                        print("\t" + p, end="\n")

            if len(files_5):
                result, list_diff = calculate(next((f for f in files_5 if f.endswith('2A')), None),
                                              next((f for f in files_5 if f.endswith('9A')), None))
                print(result)
                if result != 0:
                    for p in list_diff:
                        print("\t" + p, end="\n")

            if len(files_6):
                result, list_diff = calculate(next((f for f in files_6 if f.endswith('2A')), None),
                                              next((f for f in files_6 if f.endswith('9A')), None))

                print(result)
                if result != 0:
                    for p in list_diff:
                        print("\t" + p, end="\n")

    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("\nPress Enter to continue ...")
        input()
