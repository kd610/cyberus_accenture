import os
import pprint
import itertools
import pandas as pd


def get_binary_array(path):
    with open(path, "rb") as image:
        f = image.read()
        print(f)
        return f


def travers_path(start_path):
    id_list = []
    name_list = []
    image_list = []
    id__iter = itertools.count()

    for root, dirs, files in os.walk(start_path):
        for f in files:
            if f.endswith(".png"):
                url = root + '/' + f
                splitted_f = f.split('.')
                binary_array = get_binary_array(url)

                id_list.append(next(id__iter))
                name_list.append(splitted_f[0])
                image_list.append(binary_array)

    image_df = pd.DataFrame(
        list(zip(id_list,
                 name_list,
                 image_list,
                 )
             ),
        columns=["id", "name", "image"],
    )

    return image_df


if __name__ == '__main__':
    start_path = '/Users/hasandemirkiran/Desktop/cyberus_accenture/dataset'
    image_df = travers_path(start_path)
    print(image_df)