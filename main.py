from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import requests
import os, time
from termcolor import colored
from pyfiglet import Figlet
from webdriver_manager.chrome import ChromeDriverManager
from veritabani import Database
import math


f = Figlet(font="poison")
print(colored(f.renderText("mytsx"), "green"))

print(colored("github: https://github.com/mytsx", "red"))
print(colored("author: Mehmet YERLİ", "red"))



class Sabis():
    def __init__(self, userId, password):
        """
        Sabis sınıfının başlatma fonksiyonu.
        :param userId: Kullanıcı adı veya kimliği.
        :param password: Kullanıcının şifresi.
        """

        # Veritabanı bağlantısını başlat
        self.db = Database()

        # Kullanıcının kimliği ve şifresini sınıf değişkenlerine ata
        self.userId = userId
        self.password = password

        # İsteklerin zaman aşımına uğramasını engellemek için varsayılan bekleme süresini ayarla
        self.delay = 30  # Burada belirtildiği üzere, bu değerin 15 veya 15'in katları olması önerilir.

        # Chrome tarayıcısı için seçenekleri belirle
        options = webdriver.ChromeOptions()
        options.headless = False  # Tarayıcının başsız modda başlatılmamasını belirtir. Yani tarayıcı penceresi gözükecek.
        # Tarayıcının varsayılan indirme dizinini mevcut çalışma dizini olarak ayarla
        prefs = {
            "download.default_directory": os.getcwd(),
            "safebrowsing.enabled": "true", 
            'excludeSwitches': ['disable-logging']
        }
        options.add_experimental_option("prefs", prefs)

        # ChromeDriver'ı otomatik olarak indir ve başlat
        self.browser = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
        
        # WebDriverWait ile belirtilen süre kadar beklemeye olanak tanıyan bir bekleyici oluştur.
        self.wait = WebDriverWait(self.browser, self.delay)


    def _find_element(self, by, value):
        """
        Verilen lokatör tipi ve değeri ile eşleşen tek bir web elementini 
        bulmak için kullanılan özel (private) bir fonksiyondur.

        Parametreler:
        - by (By): Lokatörün türü. Örneğin: By.ID, By.XPATH
        - value (str): Lokatörün değeri. Örneğin bir XPATH ifadesi ya da bir ID.

        Çıktı:
        - WebElement: Eşleşen web elementi. Eşleşen bir element bulunamazsa 'None' döndürülür.

        Örnek:
        _find_element(By.XPATH, "//div[@class='someClass']") 
        -> Bu, 'someClass' sınıfına sahip ilk div elementini döndürür.
        """

        try:
            # Lokatöre eşleşen elementi bekleyerek bulma
            return self.wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            # Belirtilen süre içerisinde element bulunamazsa hata mesajı yazdır
            print("Loading took too much time!")
            return None

    def _find_elements(self, by, value):
        """
        Verilen lokatör tipi ve değeri ile eşleşen birden fazla web elementini 
        bulmak için kullanılan özel (private) bir fonksiyondur.

        Parametreler:
        - by (By): Lokatörün türü. Örneğin: By.ID, By.XPATH
        - value (str): Lokatörün değeri. Örneğin bir XPATH ifadesi ya da bir ID.

        Çıktı:
        - list: Eşleşen web elementlerinin listesi. Eşleşen element bulunamazsa boş bir liste döndürülür.

        Örnek:
        _find_elements(By.XPATH, "//div[@class='someClass']") 
        -> Bu, 'someClass' sınıfına sahip tüm div elementlerini döndürür.
        """

        try:
            # Lokatöre eşleşen tüm elementleri bekleyerek bulma
            return self.wait.until(EC.presence_of_all_elements_located((by, value)))
        except TimeoutException:
            # Belirtilen süre içerisinde elementler bulunamazsa hata mesajı yazdır
            print("Loading took too much time for multiple elements!")
            return []
    
    def find_first_element(self, locators, timeout=10):
        """
        Verilen lokatörler listesi içerisinde eşleşen web elementlerini arar.
        Belirtilen süre zarfında bulunan elementler arasından, sayfa üzerinde
        en üstte bulunanı (y eksenine göre en küçük konumu olan) döndürür.

        Parametreler:
        - locators (dict): Anahtar olarak elementin adını ve değer olarak 
                        'by' (lokatör tipi) ve 'multiple' (çoklu element mi) 
                        bilgilerini içeren bir sözlük.
        - timeout (int, optional): Arama için maksimum bekleyeceği süre. 
                                Varsayılan değeri 10 saniyedir.

        Çıktı:
        - tuple: İlk element olarak lokatörün anahtar adı, ikinci element olarak 
                bulunan web elementi. Eşleşen bir element bulunamazsa 'None' döndürülür.

        Örnek:
        locators = {
            "header": {"by": (By.XPATH, "//header")},
            "footer": {"by": (By.XPATH, "//footer")}
        }
        find_first_element(locators)
        -> Bu, sayfa üzerinde ilk olarak hangi elementin (header veya footer) 
        bulunduğunu döndürür.
        """

        found_elements = {}  # Bulunan elementleri saklamak için sözlük
        end_time = time.time() + timeout  # Aramanın sona ereceği zaman

        while time.time() < end_time:
            for key, value in locators.items():
                try:
                    # Çoklu elementler için arama
                    if value.get("multiple", False):
                        elements = self.browser.find_elements(*value["by"])
                        if elements:
                            found_elements[key] = elements[0]  # Sadece ilk elementi al
                    # Tekil element için arama
                    else:
                        element = self.browser.find_element(*value["by"])
                        if element:
                            found_elements[key] = element
                except:
                    pass

            # Bulunan elementler varsa en üstte olanı döndür
            if found_elements:
                return min(found_elements.items(), key=lambda x: x[1].location['y'])

            time.sleep(0.5)  # Kısa bir süre bekle ve tekrar ara

        return None  # Eşleşen element bulunamazsa 'None' döndür

    def visit_site(self):
        """
        Sakarya Üniversitesi'nin SABİS platformunun ana sayfasını tarayıcıda açar ve
        tarayıcı penceresini maksimize eder.

        Not: Bu fonksiyonun döndürdüğü bir değer yoktur. Sadece belirtilen web sayfasını açar.

        Örnek Kullanım:
        sabis = Sabis(user_id, password)
        sabis.visit_site()  
        -> Tarayıcıyı açar ve 'https://login.sabis.sakarya.edu.tr/Account/Login?' adresini yükler.
        """

        self.browser.get("https://login.sabis.sakarya.edu.tr/Account/Login?")  # Web sayfasını yükle
        self.browser.maximize_window()  # Tarayıcı penceresini maksimize et

    def login(self):
        """
        Sakarya Üniversitesi'nin SABİS platformuna direkt olarak giriş yapar. 
        Kullanıcının sağladığı kullanıcı adı ve şifre bilgilerini kullanarak platforma erişim sağlar.

        Not: Bu fonksiyonun döndürdüğü bir değer yoktur. Sadece belirtilen kullanıcı bilgileri 
        ile SABİS platformuna giriş yapar.

        Örnek Kullanım:
        sabis = Sabis(user_id, password)
        sabis.login()  
        -> Kullanıcı bilgileri ile SABİS platformuna giriş yapılır.
        """

        # Giriş sayfasındaki form alanlarını doldurma
        username = self._find_element(By.ID, "Username")
        pswd = self._find_element(By.ID, "Password")
        username.send_keys(self.userId)
        pswd.send_keys(self.password)

        # Giriş butonuna tıklama
        lgnBtn = self._find_element(By.XPATH, ".//button[@value='login']")
        lgnBtn.click()

    def retrieve_course_info(self):
        """
        Sakarya Üniversitesi'nin SABİS platformundan kullanıcının kayıtlı olduğu ders bilgilerini alır.
        Bu bilgileri sınıf içerisinde bir sözlük yapısında saklar, bu sözlük yapısının anahtarı dersin ismi,
        değeri ise dersin URL'si ve ID'sidir.
        
        Not: Bu fonksiyonun döndürdüğü bir değer yoktur. Sadece ders bilgilerini sınıfın içerisinde saklar.
        
        Örnek Kullanım:
        sabis = Sabis(user_id, password)
        sabis.retrieve_course_info()  
        -> Kullanıcının kayıtlı olduğu ders bilgileri alınır ve sınıf içerisinde saklanır.
        """

        # Üniversitenin OBS SABİS Ders sayfasına erişim
        self.browser.get("https://obs.sabis.sakarya.edu.tr/Ders")

        # Kullanıcının kayıtlı olduğu ders bilgilerini çekme
        courses = self._find_elements(By.XPATH, ".//div[@class='d-flex flex-row align-items-center py-1']")
        self.courses = {}

        # Çekilen ders bilgilerini sözlük yapısında saklama
        for course in courses:
            id = course.get_attribute("onclick").split("(")[1].split(")")[0]
            id = id.split(",")[0]
            course_url = f"https://obs.sabis.sakarya.edu.tr/Ders/Grup/{id}"
            course_name = course.find_element(By.TAG_NAME, "a").text
            self.courses[course_name] = (course_url, id)

        # Elde edilen ders bilgilerini konsola yazdırma
        print(self.courses)

    def download_documents(self):
        """
        Tüm dersler için belgeleri ve ders videolarını indirir. Eğer bir belge daha önce indirilmişse ve
        boyutu sayfadaki ile aynıysa tekrar indirmez. Bu sayede gereksiz yere aynı belgeyi tekrar indirmekten kaçınılır.
        """
        
        mainLoc = os.getcwd()  # Mevcut çalışma dizinini al

        # Kaydedilmiş olan her ders için
        for course_name, (course_url, id) in self.courses.items():
            self.browser.get(f"{course_url}#Dokuman")  # Dersin belgeler sayfasını aç

            # Kontrol etmek istediğimiz elementlerin lokasyon bilgisi
            locators = {
                "table_div": {"by": (By.XPATH, ".//div[@class='table-responsive']")},
                "dark_texts": {"by": (By.XPATH, ".//p[@class='text-dark-50']"), "multiple": True}
            }
            result = self.find_first_element(locators)

            if result and result[0] == "table_div":
                div = self.browser.find_element(By.XPATH, ".//div[@class='table-responsive']")
                table = div.find_element(By.TAG_NAME, "table")
                tbody = table.find_element(By.TAG_NAME, "tbody")
                rows = tbody.find_elements(By.TAG_NAME, "tr")
                
                directory_name = os.path.join(mainLoc, course_name, "documents")
                os.makedirs(directory_name, exist_ok=True)  # İndirilecek dosyalar için dizini oluştur
                os.chdir(directory_name)  # Dizine geç

                # Tablodaki her satır için (her bir satır bir belgeyi temsil eder)
                for row in rows:
                    columns = row.find_elements(By.TAG_NAME, "td")
                    anchor = columns[-1].find_element(By.TAG_NAME, "a")
                    file_type = columns[-3].text
                    file_name = columns[1].text
                    file_url = anchor.get_attribute("href")
                    file_material_size_page = columns[6].text  # Sayfada gösterilen dosya boyutu
                    local_filename = f"{file_name}{file_type}"

                    # Dosyanın daha önce indirilip indirilmediğini kontrol et
                    is_downloaded = self.db.check_downloaded(course_name, file_name, file_material_size_page)
                    local_filename_with_path = os.path.join(directory_name, local_filename)
                    file_exists_on_disk = os.path.exists(local_filename_with_path)

                    # Dosyanın daha önce indirildiğini ve boyutunun doğru olduğunu kontrol et
                    if is_downloaded and file_exists_on_disk:
                        file_size_on_disk = int(os.path.getsize(local_filename_with_path) / 1024)
                        if math.isclose(file_size_on_disk, int(file_material_size_page), abs_tol=1.0):
                            print("dosya zaten var", file_name)
                            continue
                    
                    print("indiriliyor", file_name)
                    self.download_file(file_url, local_filename)
                    # İndirilen dosyanın bilgileri veri tabanına kaydedilir.
                    self.db.insert_download(course_name, file_name, file_material_size_page, local_filename_with_path)

                os.chdir(mainLoc)  # Ana dizine geri dön
            else:
                print(f"No documents found for course {course_name}")

        self.db.close()  # Veritabanı bağlantısını kapat

    def download_file(self, url, filename):
        """
        Belirtilen URL'den dosya indirir ve belirtilen dosya adıyla kaydeder.
        
        Parametreler:
            - url (str): İndirilecek dosyanın URL adresi.
            - filename (str): İndirilen dosyanın kaydedileceği dosya adı.
        
        İşlev:
            - Verilen URL adresinden dosyayı "stream" modunda indirir.
            - Dosyayı parça parça (chunk) okur. Her bir parça için belirli bir boyut (örn. 8192 byte) kullanılır.
            - Okunan her bir parçayı belirtilen dosya adıyla diske yazar.
            - Böylece büyük dosyaların bile bellekte çok fazla yer kaplamadan indirilmesi sağlanır.
        """
        with requests.get(url, stream=True) as r:  # "stream" modunda dosyayı indir
            r.raise_for_status()  # Eğer bir hata varsa (örn. 404 Not Found), exception fırlat
            with open(filename, 'wb') as f:  # İndirilen dosyayı yazma ve binary modunda aç
                for chunk in r.iter_content(chunk_size=8192):  # Dosyayı parça parça oku
                    f.write(chunk)  # Okunan parçayı diske yaz

    def close_browser(self):
        """
        Tarayıcı penceresini kapatır.
        
        İşlev:
            - Bu fonksiyon, Selenium webdriver'ın (tarayıcının) "close" metodunu kullanarak
            aktif tarayıcı penceresini kapatır. Eğer tarayıcıda birden fazla sekme veya pencere 
            açık ise sadece aktif olan pencereyi kapatır. Diğer pencereler etkilenmez.
        """
        self.browser.close()


if __name__ == "__main__":
    """
    Bu koşul, bu script dosyası doğrudan çalıştırıldığında gerçekleşecek olan
    işlemleri tanımlar. Bu dosya başka bir dosya tarafından import edildiğinde
    bu kısım çalıştırılmaz.
    """
    
    # 'bilgiler.txt' adlı dosyayı okuma modunda aç
    with open("bilgiler.txt", "r") as f:
        # Dosyanın içerisindeki her bir satırı oku, strip ile satır sonu karakterlerini kaldır
        # ve bu bilgileri user_id ve password değişkenlerine ata
        user_id, password = [line.strip() for line in f.readlines()]

    # Sabis sınıfından bir nesne oluştur ve bu nesneye kullanıcı adı ve şifreyi parametre olarak ver
    sabis = Sabis(user_id, password)

    # Aşağıdaki fonksiyonlar, oluşturulan sabis nesnesi üzerinde belirtilen sırayla çağrılır.
    
    sabis.visit_site()  # Sabis web sitesini ziyaret et
    sabis.login()  # Sabis web sitesine giriş yap
    sabis.retrieve_course_info()  # Kurs bilgilerini al
    sabis.download_documents()  # Kurs dokümanlarını indir
    sabis.close_browser()  # Tarayıcıyı kapat

    # İşlem tamamlandığında kullanıcıya bilgi vermek amacıyla bir mesaj yazdır.
    print("TÜM DERS NOTLARI İNDİRİLDİ")
