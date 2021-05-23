import pandas as pd


def get_length(square, clusters):
    result = []
    for i in clusters:
        result.append(abs(square[1] - i))
    min_delta = min(result)
    i_min_delta = result.index(min_delta)
    return i_min_delta


def print_data(result, y):
    ''' result_museum_distribution.append([clusters, distribution]) '''
    print('''              Изменение Кластеров по эпохам \n''')
    for (i, j) in zip(range(len(y)), y):
        print('Эпоха', i, ' ' * (3 - len(list(str(i)))), '  | Центры кластеров: ', end=' ')
        for z in j:
            print(round(z, 3), ' ' * (15 - len(list(str(round(z, 3))))), end='')
        print()

    print('''\n\n\n                   Получившееся разбиение\n\n''')
    for (i, j) in zip(result[-1][0], result[-1][1]):
        print('                      Центр кластера: ', round(i, 3), 'м²\n\n')
        j = sorted(j, key=lambda o: o[1])
        for j in j:
            print('Музей: ', j[0], ' ' * (90 - len(list(j[0]))), ' Площадь: ', j[1], 'м²')
        print('\n\n\n')


class NeuralSiteKohonena:

    def __init__(self, data, clusters):
        y = [[], sorted(clusters)]
        result_museum_distribution = []
        while y[-1] != y[-2]:
            data_distribution = []
            for d in data:
                data_distribution.append(get_length(d, y[-1]))

            distribution = []
            for i in range(len(y[-1])):
                distribution.append([])

            for (i, j) in zip(data, data_distribution):
                distribution[j].append(i)
            result_museum_distribution.append([y[-1], distribution])
            new_clusters = []
            for museums in distribution:
                if len(museums) != 0:
                    sr_square = 0
                    for museum in museums:
                        sr_square += museum[1]
                    sr_square /= len(museums)
                    new_clusters.append(sr_square)
            y.append(sorted(new_clusters))
        print_data(result_museum_distribution, y[1:])


if __name__ == '__main__':

    df = pd.read_excel(r'data.xlsx', engine='openpyxl', na_filter=False)
    df = df[df['LandArea'] != '']
    df = df[['CommonName', 'LandArea']].values.tolist()
    for d in df:
        d[1] = float(d[1])
    for i in df:
        print('Музей: ', i[0], ' ' * (90 - len(list(i[0]))), ' Площадь: ', i[1], 'м²')

    clusters = [300, 500, 1000, 3000, 10000, 30000, 100000]
    # clusters = [int(item) for item in input(" ВВедите центры: ").split(' ')]
    print('\n\nClusters:', clusters)
    print('\n\n\n\n')
    n = NeuralSiteKohonena(df, clusters)
