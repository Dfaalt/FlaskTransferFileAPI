from db import get_db_connection

def insert_image_blob(filename, image_blob):
    db = get_db_connection()
    cursor = db.cursor()
    query = "INSERT INTO screenshots (filename, image_data) VALUES (%s, %s)"
    cursor.execute(query, (filename, image_blob))
    db.commit()
    db.close()

def get_latest_image_blob():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, filename, image_data, created_at FROM screenshots ORDER BY created_at DESC LIMIT 1")
    result = cursor.fetchone()
    db.close()
    return result

def get_all_images_blob():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, filename, created_at FROM screenshots ORDER BY created_at DESC")
    result = cursor.fetchall()
    db.close()
    return result

def delete_image_blob(id=None, all_data=False):
    db = get_db_connection()
    cursor = db.cursor()

    if all_data:
        cursor.execute("DELETE FROM screenshots")
        deleted_count = cursor.rowcount
    else:
        cursor.execute("DELETE FROM screenshots WHERE id = %s", (id,))
        deleted_count = cursor.rowcount

    db.commit()
    db.close()
    return deleted_count

    
