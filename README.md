# CSV to MySQL Database Import Script

A Python script to import data from CSV file to MySQL database. Specifically handles sender and their related arwah data.

## Requirements

- Python 3.x
- MySQL Server
- Required Python packages:
  ```bash
  pip install mysql-connector-python pandas
  ```

## Usage

1. Set up your database configuration:
```python
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'your_database'
}
```

3. Run the script:
```bash
python import_csv.py
```

## How It Works

1. Reads CSV file using pandas
2. For each row in CSV:
   - Inserts sender data into `senders` table
   - Gets the newly created sender ID
   - Inserts arwah data into `arwahs` table with reference to sender ID
3. Uses transaction system to ensure data integrity
4. Handles errors with proper rollback

## License
Licensed under the MIT License.
