import os
import sys
import pandas as pd
import numpy as np
from collections import Counter
from itertools import chain

files = []
path_files = ""
list_diff_ocu = []
count_two = 0


def more_events(val, file_nine):
    count_occurrences = (val.iloc[0]['e'].astype(int) -
                         val.iloc[0]['d'].astype(int)) + 1

    count_two += count_occurrences

    occurrences_found = int(open(path_files + file_nine, 'r').read()
                            .count(val.iloc[0]['combined']))

    difference = occurrences_found - count_occurrences

    if difference != 0:
        list_diff_ocu.append(val.iloc[0]['combined'] + ": "
                             + str(difference))


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
    folio_duplicate = []

    my_data = pd.read_csv(path_files + file_two, decimal=",", skiprows=1,
                          usecols=(4, 5, 6, 8, 9), names=["a", "b", "c", "d", "e"])

    df_with_zeros = pd.DataFrame(my_data)

    df = pd.DataFrame()

    for i, row in df_with_zeros.iterrows():
        if row.d != 0 and row.e != 0:
            df = df.append(row)

    df["combined"] = df["a"].astype(str) + "," \
        + df["b"].astype(str) + "," + df["c"]

    df_occur = pd.DataFrame()
    df_occur['freq'] = df['combined'].value_counts()

    for i, row in df_occur.iterrows():
        # Para carriles que no tienen mas de dos folios de inicio en el archivo
        if row.freq < 2:
            val = df[df['combined'] == row.name]
            # Logica para saber eventos de mas
            more_events(val, file_nine)
        else:
            val = df[df['combined'] == row.name]
            vals = []
            for d, e in zip(val.d, val.e):
                vals.append(e)
                vals.append(d)

            df1 = pd.DataFrame({'combined': vals})

            df_occur1 = pd.DataFrame()
            df_occur1['freq'] = df1['combined'].value_counts()

            print(df_occur1)
            # PENDIENTE: PREGUNTAMOS SI HAY OCURR MAYOR A 2, SI ES VERDAD ENTONCES MANDAMOS A LISTA DE DE FOLIOS
            # SI NO, RECORREMOS UNA POR UNA LAS FILAS DE VAL

    # Sacamos diferencia
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


#    for index, row in df_occur.iterrows():
#         if row.freq < 2:
#             val = df[df['combined'] == row.name]
#             if val.iloc[0]['e'].astype(int) != 0 and val.iloc[0]['d'].astype(int) != 0:
#                 # Logica para saber eventos de mas
#                 count_occurrences = (val.iloc[0]['e'].astype(
#                     int) - val.iloc[0]['d'].astype(int)) + 1

#                 count_two += count_occurrences

#                 occurrences_found = int(open(path_files + file_nine, 'r').read()
#                                         .count(row.name))

#                 difference = occurrences_found - count_occurrences

#                 if difference != 0:
#                     list_diff_ocu.append(
#                         row.name + ": " + str(difference))
#         else:
#             val = df[df['combined'] == row.name]
#             val = val.reset_index(drop=True)

#             val1 = pd.DataFrame()
#             for idx, r in val.iterrows():
#                 if r.e != 0 and r.d != 0:
#                     val1 = val1.append(r)

#             if len(val1) < 2:
#                 # Logica para saber eventos de mas
#                 count_occurrences = (val1.iloc[0]['e'].astype(
#                     int) - val1.iloc[0]['d'].astype(int)) + 1

#                 count_two += count_occurrences

#                 occurrences_found = int(open(path_files + file_nine, 'r').read()
#                                         .count(val1.iloc[0]['combined']))

#                 difference = occurrences_found - count_occurrences

#                 if difference != 0:
#                     list_diff_ocu.append(
#                         val1.iloc[0]['combined'] + ": " + str(difference))
#             else:
#                 vals = []
#                 for d, e in zip(val.d, val.e):
#                     vals.append(e)
#                     vals.append(d)

#                 df1 = pd.DataFrame({'combined': vals})

#                 df_occur1 = pd.DataFrame()
#                 df_occur1['freq'] = df1['combined'].value_counts()

#                 print(df_occur1)
