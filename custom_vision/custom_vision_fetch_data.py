import sqlalchemy as db
import pickle

engine = db.create_engine(
    "postgresql://hasan@cyberus:cyberus-123@cyberus.postgres.database.azure.com:5432/postgres"
)
connection = engine.connect()
metadata = db.MetaData()


def getTable(table_name):
    arr = []
    table = db.Table(table_name, metadata, autoload=True, autoload_with=engine)
    query = db.select([table])
    result = connection.execute(query).fetchall()
    for row in result:
        arr.append(row)
    with open(table_name, 'wb') as fp:
        pickle.dump(arr, fp)


getTable("defect_images")
getTable("defect_images_black_white")
getTable("defect_images_denoising")
getTable("defect_images_gamma_correction")
getTable("defect_images_histogram_equalization")
getTable("defect_images_preprocess_all")
getTable("normal_images")
getTable("normal_images_black_white")
getTable("normal_images_denoising")
getTable("normal_images_gamma_correction")
getTable("normal_images_histogram_equalization")
getTable("normal_images_preprocess_all")

