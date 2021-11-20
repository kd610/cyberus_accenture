from sqlalchemy import *
from extract_info import travers_path
 
if __name__ == '__main__':
    # Creating SQLAlchemy's engine to use
    engine = create_engine(
        "postgresql://hasan@cyberus:cyberus-123@cyberus.postgres.database.azure.com:5432/postgres"
    )

    start_path_normal = '/Users/hasandemirkiran/Desktop/cyberus_accenture/dataset/normal'
    start_path_defect = '/Users/hasandemirkiran/Desktop/cyberus_accenture/dataset/defect'

    normal_image_df = travers_path(start_path_normal)
    defect_image_df = travers_path(start_path_defect)

    normal_image_df.to_sql(
        "normal_images",
        engine,
        if_exists="append",
        index=False
    )

    defect_image_df.to_sql(
        "defect_images",
        engine,
        if_exists="append",
        index=False
    )