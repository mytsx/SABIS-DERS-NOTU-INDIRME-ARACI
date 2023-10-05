import sqlite3

class Database:
    def __init__(self, db_name="downloads.db"):
        """
        Database sınıfının başlatma fonksiyonu.
        :param db_name: Veritabanı dosyasının adı. Eğer belirtilmezse 'downloads.db' olarak varsayılır.
        """
        self.conn = sqlite3.connect(db_name)  # SQLite veritabanı bağlantısını başlat.
        self.cursor = self.conn.cursor()  # Bir cursor (imleç) oluştur, bu imleç üzerinden SQL sorguları çalıştırılabilir.
        self.create_table()  # Veritabanında tablo oluştur.

    def create_table(self):
        """
        Veritabanında 'downloads' adında bir tablo oluştur.
        Bu tablo, daha önce indirilmiş dosyaların bilgilerini saklamak için kullanılır.
        """
        # Eşsiz bir anahtar olarak kullanılan otomatik artan bir sayı.
        # Dersin adı.
        # Dosyanın adı.
        # Dosya boyutu.
        # Dosyanın yerel dosya sistemindeki yolu.
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY,  
            course_name TEXT NOT NULL,  
            file_name TEXT NOT NULL,  
            file_material_size TEXT NOT NULL, 
            local_path TEXT NOT NULL  
        )
        """)
        self.conn.commit()  # Değişiklikleri kaydet.

    def insert_download(self, course_name, file_name, file_material_size, local_path):
        """
        Veritabanına yeni bir indirme kaydı ekler.
        :param course_name: Dersin adı.
        :param file_name: Dosyanın adı.
        :param file_material_size: Dosyanın boyutu.
        :param local_path: Dosyanın yerel yoldaki konumu.
        """
        self.cursor.execute("INSERT INTO downloads (course_name, file_name, file_material_size, local_path) VALUES (?, ?, ?, ?)",
                            (course_name, file_name, file_material_size, local_path))
        self.conn.commit()  # Değişiklikleri kaydet.

    def check_downloaded(self, course_name, file_name, file_material_size):
        """
        Belirtilen parametrelere sahip bir dosyanın daha önce indirilip indirilmediğini kontrol eder.
        :param course_name: Kontrol edilmek istenen dersin adı.
        :param file_name: Kontrol edilmek istenen dosyanın adı.
        :param file_material_size: Kontrol edilmek istenen dosyanın boyutu.
        :return: Eğer dosya daha önce indirilmişse dosyanın yerel yolunu döndürür. Aksi halde None döndürür.
        """
        self.cursor.execute("SELECT local_path FROM downloads WHERE course_name = ? AND file_name = ? AND file_material_size = ?",
                            (course_name, file_name, file_material_size))
        return self.cursor.fetchone()  # Eşleşen ilk sonucu döndür.

    def close(self):
        """
        Veritabanı bağlantısını kapatır.
        """
        self.conn.close()
