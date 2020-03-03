import os
import sys
import pandas as pd

files = []
path_files = ""
list_diff_ocu = []
count_two = 0


def more_events(val, file_nine, lane_dupli=False):
    global count_two
    if lane_dupli:
        count_occurrences = 0
        for i, r in val.iterrows():
            count_occurrences += (r.e - r.d) + 1

        count_two += count_occurrences
        occurrences_found = int(open(path_files + file_nine, 'r').read()
                                .count(val.head(1).iloc[0]['combined']))

        difference = occurrences_found - count_occurrences

        if difference != 0:
            list_diff_ocu.append(val.head(1).iloc[0]['combined'] + ": "
                                 + str(difference))
    else:
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
    #path_files = sys.argv[1] + '\\'

    list_files = [f for f in os.listdir(path_files)]

    if len(list_files) < 2:
        raise ValueError(
            'should be only one 9A or 2A file in the current directory')

    global files
    files = list(filter(lambda x: x.endswith("2A")
                        or x.endswith("9A"), list_files))


def calculate(file_two, file_nine):
    my_data = pd.read_csv(path_files + file_two, decimal=",", skiprows=1,
                          usecols=(4, 5, 6, 8, 9), names=["a", "b", "c", "d", "e"])

    df = pd.DataFrame(my_data)

    indexs = df[(df['d'].astype(int) == 0) & (df['e'].astype(int) == 0)].index

    df.drop(index=indexs, inplace=True)

    df["combined"] = df["a"].astype(str) + "," \
        + df["b"].astype(str) + "," + df["c"]

    df_occur = pd.DataFrame()
    df_occur['freq'] = df['combined'].value_counts()

    list_folios_duplic = None
    # Para carriles que no tienen mas de dos folios de inicio en el archivo
    for i, row in df_occur.iterrows():
        val = df[df['combined'] == row.name]
        if row.freq < 2:
            more_events(val, file_nine)
        else:
            vals = []
            for d, e in zip(val.d, val.e):
                vals.append(e)
                vals.append(d)

            df1 = pd.DataFrame({'combined': vals})

            df_occur1 = pd.DataFrame()
            df_occur1['freq'] = df1['combined'].value_counts()

            folio_duplic = df_occur1[df_occur1['freq'] > 1].index.tolist()

            # PENDIENTE: PREGUNTAMOS SI HAY OCURR MAYOR A 2, SI ES VERDAD ENTONCES MANDAMOS A LISTA DE DE FOLIOS
            # SI NO, RECORREMOS UNA POR UNA LAS FILAS DE VAL Y SI NO, SUMAMOS Y BUSCAMOS

            if len(folio_duplic):
                df2 = val[(val['d'].astype(int) == folio_duplic[0]) |
                          (val['e'].astype(int) == folio_duplic[0])]
                if len(df2):
                    list_folios_duplic = df2[[
                        'combined', 'd', 'e']].values.tolist()
                else:
                    more_events(val, file_nine, True)
            else:
                more_events(val, file_nine, True)

    if list_folios_duplic is None:
        # Sacamos diferencia
        header_nine = ''
        with open(path_files + file_nine, 'r') as f:
            header_nine = f.readline()

        result = "Turno " + file_two[-3] + ": " + \
            str(int(header_nine[-6:]) - count_two)

        return result, list_diff_ocu
    else:
        result = "Turno " + file_two[-3] + " con folios duplicados"
        return result, list_folios_duplic


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
                        print(f"\t{p}", end="\n")

                list_diff_ocu = []
                count_two = 0

            if len(files_5):
                result, list_diff = calculate(next((f for f in files_5 if f.endswith('2A')), None),
                                              next((f for f in files_5 if f.endswith('9A')), None))
                print(result)
                if result != 0:
                    for p in list_diff:
                        print(f"\t{p}", end="\n")

                list_diff_ocu = []
                count_two = 0

            if len(files_6):
                result, list_diff = calculate(next((f for f in files_6 if f.endswith('2A')), None),
                                              next((f for f in files_6 if f.endswith('9A')), None))
                print(result)
                if result != 0:
                    for p in list_diff:
                        print(f"\t{p}", end="\n")

                list_diff_ocu = []
                count_two = 0

    except BaseException:
        import sys
        print(sys.exc_info()[0])
        import traceback
        print(traceback.format_exc())
    finally:
        print("\nPress Enter to continue ...")
        input()
