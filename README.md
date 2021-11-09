# Seed coupon table for inContract

First, install the required packages:

```shell
pip install -r requirements.txt
```

To use the script, make sure you have the following environment variables set:

- `INSTANCE_CONNECTION_NAME`, if you are using production.
- `PROD_USER`, the user to use when connecting to production database.
- `PROD_PASSWORD`, the password to use when connecting to production database.
- `PROD_DATABASE`, the name of the database to use when connecting to production database.
- `LOCAL_USER`, the user to use when connecting to local database.
- `LOCAL_PASSWORD`, the password to use when connecting to local database.
- `LOCAL_DATABASE`, the name of the database to use when connecting to local database.

Simply, set the environment variables and run the script.

```shell
export ENV_VARIABLE=VALUE
python main.py
```

If you want to use the script for the production database, make sure to update the main function:

```python
if __name__ == '__main__':
  seed_coupons(prod=True)
```

This will allow run the script for the production database.
