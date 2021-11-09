import csv
import datetime
import os
import random
import string
import urllib.request
from sys import platform

import MySQLdb


def run_proxy() -> None:
    # Download the cloud_sql_proxy.
    urllib.request.urlretrieve(f'https://dl.google.com/cloudsql/cloud_sql_proxy.{platform}.amd64',
                               'cloud_sql_proxy')
    # Make the file executable.
    os.system('chmod +x cloud_sql_proxy')

    # Use credentials.
    os.system('export GOOGLE_APPLICATION_CREDENTIALS=./prod-gcloud-key')

    # Run proxy
    instance = os.environ['INSTANCE_CONNECTION_NAME']
    os.system(f'./cloud_sql_proxy -instances "{instance}"=tcp:0.0.0.0:1234 &')


def connect_database(host: str, port: int, user: str, password: str, database: str) -> MySQLdb.connect:
    """
    Connect to the database.
    :param host: Database host.
    :param port: Database port.
    :param user: Username.
    :param password: Password.
    :param database: Database name.
    :return:
    """
    return MySQLdb.connect(host=host, port=port, user=user, password=password, db=database)


def seed_coupons(amount_of_coupons: int = 100, expires_in: int = 90, discount: int = 100, prod: bool = False) -> None:
    """
    Seed the coupons table.

    :param amount_of_coupons: The number of coupons to seed.
    :param expires_in: Expiry date in days.
    :param discount: Discount percentage.
    :param prod: If True, seeds the prod database.
    """
    # If production run the proxy and use the production database.
    if prod:
        run_proxy()

    db = connect_database(host="localhost",
                          port=1234 if prod else 3306,
                          user=os.environ['PROD_USER'] if prod else os.environ['LOCAL_USER'],
                          password=os.environ['PROD_PASSWORD'] if prod else os.environ['LOCAL_PASSWORD'],
                          database=os.environ['PROD_DATABASE'] if prod else os.environ['LOCAL_DATABASE'])
    cur = db.cursor()

    now = str(datetime.datetime.today())
    expired_on = str(datetime.datetime.today() + datetime.timedelta(days=expires_in))

    # Headers for the CSV file.
    header = ['CODE', 'DATE_CREATED', 'EXPIRY_DATE']
    rows = []

    for i in range(amount_of_coupons):
        code = ''.join(random.choice(string.ascii_uppercase) for _ in range(6))

        row = [code, now, expired_on]
        rows.append(row)

        cur.execute(f"INSERT INTO coupon VALUES (default, null, '{code}', '{now}', {discount}, null, "
                    f"'{expired_on}', null)")

    db.commit()

    # Write to the CSV file.
    with open('coupons.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)

    db.close()


if __name__ == '__main__':
    seed_coupons()