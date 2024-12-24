import mysql.connector
import pandas as pd
from datetime import datetime

# Konfigurasi koneksi ke database MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_kanggotan2'
}

def insert_data_to_db(csv_file):
    # Current timestamp (UTC)
    current_timestamp = '2024-12-24 11:45:57'
    
    # Membaca CSV
    df = pd.read_csv(csv_file)
    
    # Membuka koneksi ke database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    current_sender_id = None

    try:
        # Memasukkan data ke tabel senders
        for index, row in df.iterrows():
            sender_name = row['SENDER NAME'] if pd.notna(row['SENDER NAME']) else None
            address = row['ADDRESS'] if pd.notna(row['ADDRESS']) else None
            phone = None  # Karena tidak ada di CSV
            
            if sender_name is not None:
                cursor.execute("""
                    INSERT INTO senders (name, phone, address, created_at, updated_at)
                    VALUES (%s, %s, %s, %s, %s)
                """, (sender_name, phone, address, current_timestamp, current_timestamp))
                
                current_sender_id = cursor.lastrowid

            # Memasukkan data ke tabel arwah
            if pd.notna(row['ARWAH NAME']):
                arwah_name = row['ARWAH NAME']
                arwah_address = row['MAKAM'] if pd.notna(row['MAKAM']) else ''  # Default empty string karena NOT NULL
                
                if current_sender_id is not None:
                    cursor.execute("""
                        INSERT INTO arwahs (sender_id, arwah_name, arwah_address, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (current_sender_id, arwah_name, arwah_address, current_timestamp, current_timestamp))

        conn.commit()
        print("Data berhasil dimasukkan ke database.")

    except Exception as e:
        conn.rollback()
        print(f"Error: {str(e)}")
        raise

    finally:
        cursor.close()
        conn.close()

# Menjalankan fungsi dengan file CSV
csv_file = 'source/data.csv'
try:
    insert_data_to_db(csv_file)
except Exception as e:
    print(f"Terjadi kesalahan: {str(e)}")