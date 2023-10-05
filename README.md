# Sabis Otomasyon

Sabis Otomasyon, Sakarya Üniversitesi'nin Sabis platformuna otomatik olarak giriş yaparak ders bilgilerini ve dokümanları indirmenizi sağlayan bir Python aracıdır.

## Başlangıç

Bu bölüm, Sabis Otomasyon'un nasıl kurulacağı ve çalıştırılacağı hakkında bilgiler içermektedir.

### Önkoşullar

Bu aracı çalıştırmak için öncelikle Python'ın bilgisayarınıza yüklü olması gerekmektedir. Eğer Python yüklü değilse, [Python resmi web sitesi](https://www.python.org/downloads/) üzerinden indirip kurabilirsiniz. Kurulum sırasında `PATH`'e Python eklemeyi unutmayın.

Daha sonra, aşağıdaki Python kütüphanelerine ihtiyacınız vardır:

- `selenium`
- `requests`
- `webdriver_manager`

Bu kütüphaneleri pip aracılığıyla şu şekilde yükleyebilirsiniz:

```bash
pip install selenium requests webdriver_manager
```

### Kurulum ve Çalıştırma

1. Bu repoyu git clone komutu ile lokal makinanıza kopyalayın veya zip olarak indirip çıkarın.
2. bilgiler.txt dosyasını oluşturun ve ilk satırına `kullanıcı adınızı`, ikinci satırına `şifrenizi` yazın.
3. main.py dosyasını çalıştırın.

```bash
python main.py
```

### Aracın İşleyişi

Bu araç Sabis sınıfı üzerinde çalışır. Temelde, belirtilen kullanıcı adı ve şifre ile Sabis platformuna giriş yapar. Ardından ders bilgilerini çeker ve belirtilen derslere ait dokümanları indirir.

 - visit_site: Sakarya Üniversitesi'nin ana sayfasını ziyaret eder.
 - login: Kullanıcı adı ve şifre kullanarak siteye otomatik giriş yapar.
 - retrieve_course_info: Mevcut derslerin bilgilerini çeker.
 - download_documents: Belirtilen derslerin dokümanlarını indirir.
 - download_file: Belirli bir dosyanın URL'sini kullanarak dosyayı indirir.
 - close_browser: Tarayıcıyı kapatır.

### Veritabanı İşlevselliği

Sabis Otomasyon aracı, indirilen dosyaları ve onların meta verilerini (dosya adı, boyutu, ilgili ders vb.) takip etmek için SQLite3 tabanlı bir veritabanı kullanır. Bu veritabanı işlevselliği sayesinde, program daha önceden indirilmiş bir dosyanın farkında olabilir ve bu dosyanın tekrar indirilmesini engeller. Eğer belirli bir ders materyali daha önceden indirildiyse ve yerel diskte bu materyalin boyutu ile Sabis platformunda listelenen materyalin boyutu aynıysa, bu dosyanın tekrar indirilmesine gerek kalmaz. Bu, gereksiz indirmeleri önlemek ve daha hızlı bir kullanıcı deneyimi sunmak için kritiktir.

### Lisans

Bu proje MIT lisansı altındadır - detaylar için [LİSANS](https://github.com/mytsx/SABIS-DERS-NOTU-INDIRME-ARACI/blob/main/LICENSE) dosyasına bakınız.
