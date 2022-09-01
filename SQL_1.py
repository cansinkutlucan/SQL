#%% SQL-1. ders_01.06.2022_ İlk konu anlatım dersi(Kurulumdan sonraki ilk ders)

# https://lms.clarusway.com/mod/page/view.php?id=21583
"""
1. SQL Basics Covered in 10 Minutes
2. Zachary Thomas’ SQL Questions
3. Select * SQL
4. Leetcode
5. LinkedIn Learning
6. Window Functions
7. HackerRank
8. W3 Schools
9. CodeAcademy
10. SQLZoo
11. SQL Bolt
"""
"""
The main layer we interact with SQL Server is Database Engine. Database Engine consists of two components:
    Relational Engine (Query Processor) and Storage Engine. Relational Engine is responsible for executing queries.
    Storage Engine manages database objects such as view, trigger, stored procedure.
"""



###### KABACA KONU AKIŞI
# KONSEPTLER(Relational Database Concepts)
# MANAGEMENT STUDIO(SQL Server Management studio kısa bilgi)
# INTEGRITY RULES(Integrity Rules)
# BUSINESS RULES(Integrity Rules başlığı altında bir başlık)
# ENTITY RELATIONSHIP DIAGRAM
# CONSTRAINTS
# NORMALIZATION

#%%
# SQL de verinin temin edilmesi, verinin planlanmış ortamda tutulması verinin modellenmesi, veritabanının modellenmesi önem arz ediyor.
# .. Bunlarla uğraşmayacaksınız ama bilmekte çok fayda var. Veriyi çekerken kısa sürede bunları yapmak için veritabanı çalışma
# .. mantığını iyi bilmemiz gerekiyor.

# Table of Contents
# A.Relational Database Concepts
# B.Integrity Rules
# C.Normalization

#%% A.Relational Database Concepts 
# TERIMLER : Data, Table, Relations, Relationships, Domain, Column,
# .. Row, Normalization, ERD, Integrity Rules, Constraints, Data types
# NOT: Bazı terimlerin akılda kalması sürebilir bu derste ama zamanla alışacağız
# RDBM: Bir takım nesnelerin birbirleri ile olan ilişkileri

# Veri structured olabilir, text olabilir , video olabilir vs. ama  Biz structured veri üzerinde
# .. SQL programlama dilini çalıştıracağız. (Yani mesela bir dosya üzerinde SQL çalışması yapmayacağız)

"""
# Data(Structured)
Std_Id   First Name     Last Name       Email
1109        ...            ....           ...
1401
1756
...
...
"""
# Database: Veri tablolarının bulunduğu mantıki bir küme
# .. Müşteriye hizmete yönelik ilgili tabloların varolduğu yapıya database diyoruz

# Metadata: Verinin hakkındaki veri. Yani, bir tablomuz var diyelim. Tablo içinde kitapların listesi var
# .. Bu tablonun içine bakınca bu tablonun içeriğidir(Metadata değildir). 
# .. Bu tabloda kaç satır/sütun var, kim düzenlemiş, doğum tarihi sütunu hangi yılları kapsıyor
# .. bu data ne zaman oluşturulmuş gibi bilgiler metadatadır. Bu metadata bazen çok işe yarıyor

# Domain: Örneğin isim sütununun domain bilgleri; veri tipi "text" tir, bir sütunda birden fazla kişiye ait isim yoktur vs vs
# .. Tarih dediğimizde tarihin yazım şeklinde olmalıdır veri ya da tarihin anlamını bilmeliyiz vs.

# Table:Veriyi bir arada içeren sütun ve satırlarda oluşan yapı

# Table Properties - 1
# 1.Tablo ismi unique() olmalı. Aynı isme ait 2. bir tablo tanımlayamayız
# 2.Duplicate satır olmamalı
# 3.Columns are atomic. YaniBir kişinin birden fazla numarası telnosu varsa hücre 
# .. içine tek bir telno yazabilirim. Başka telno varsa başka hücreye yazmalıyım
# 4.Veri tipleri aynı olmalı: Veri tipi: nümerik ise oraya "+90" ile başlayan bir şey yazamayız mesela

# Table Properties - 2
# 1. Bir sütun içerisinde 2 farklı veri tipi yer alamaz
# 2. Her bir attribute un farklı(distinct) ismi vardır
# 3. Sütun sırası önemsiz
# 4. Satır sırası önemsiz

# Columns : Sütunlar/Kolonlar. Her bir kolon bir özelliği ifade ediyor
# Row/Record/Tuple : Satırlar

# Relation: Bir kişiyi ifade eden değer bulmaya çalışıyoruz. ya da, country tablosunda, country_id ayrı ülkeleri
# .. temsil ediyor. Diğer sütunda region_id varsa sadece bu bilgi yeter. Çünkü region bilgisi
# .. başka bir sütunda tutuluyor bunları da country tablosuna yazmama gerek yok

#%% MS SQL bilgi ve notlar
# Microsoft SQL Server Management Studio hakkında bilgi
# Buna bir database tanımlamamız gerekiyor bunu da management studio ile halledeceğiz
# SQL Server Authencation ile o veritabanında tanımlanmış bir kullanıcı ile bağlantı kurabilirim
# İçinde database, tablolar vs hepsini görebiliyorum
# Tablolar ile ilgili sorgu yapmak için yukarıda "new query" ye tıklayabiliriz
# Query ekranını "sarı renkli" yere(bara) tıklayarak yerini değiştirebiliriz
# Burada yazdığım sorgular sol üstte boşlukta("SampleRetain") yazan database e gidiyor
# Sorgu yazdıktan sonra sorguyu mouse ile seçip üstte "execute" a tıklayarak sorguyu çalıştırabilirim
# Altta sorgu sonucumuzu görüyoruz.
# Solda database in altındaki database diagrama sağ tıklıyoruz(SampleRetail)--> new database diagram
# .. Tüm sütunları seç--> add .. Burada tablolar arasındaki bağlantıları görüyoruz
# Tools-options-(arama kelimesi)line -- line numbers ı işaretlediğimzde satır numaralarını görebiliriz query de
# Query leri "Ctrl + S" ile kaydedebiliriz ya da çarpı işaretine bastığımızda "yes" diyerek kaydedebiliriz

#%% B.Integrity Rules
# B.1 Database Rules
# Database tarafından tanımlanmış olan bütünlüğü sağlamak için kurallarla ilgili varsayımlar

# 1.Domain integrity: Domain olarak sütunu düşünebiliriz burada
# ..  Örneğin bir sütun düşünelim std_ID , integer olarak tanımlanmış ama altta
# .. integer olmayan değerler varsa burada domain integrity yi korumak için bunların hepsi integer olmalı
# .. zaten integer olarak belirlenseydi buraya string ifade giremezdik
# 2.Entity integrity: Aynı sütunu düşünelim. std_ID de bir kayıt var ama boş olamaz
# .. Her satırda farklı bir Id bulunmalı
# 3.Referential integrity: Sipariş tablomuzda. Kendinizde olmayan bir ürünü bir müşteriye satamayız
# .. Bir ürünüm varsa bunun kesinlikle ürün tablomda olması gerekiyor. Eğer ürün tablosunda
# .. olmayan id yi girersem o bütünlüğü sağlayamam. Buna da Referential integrity deniyor
# 4.Exterprise Constraints:Database administratorların kullandığı bir alan Bunu çok bilmemize gerek yok.

# NOT: Yukardaki ilk 3 ünü bilsek yeterli. Bunları çok kullanmayacağız ama bunları bilmemiz bize
# .. SQL de çalışırken bir çok şey rahat anlamamızı sağlayacak 

################################################################
# B.2 Businesss Rules
# Business tarafından tanımlanmış olan bütünlüğü sağlamak için kurallarla ilgili varsayımlar

# Örneğin bir firma Her bir siparişte sadece 1 ürün satabilirim
# Örneğin başka bir firma her bir siparişte sadece 5 ürün satabilirim
# Örneğin başka bir firma her bir siparişte sadece 1 kalem satabilirim. Yeni kalem için yeni sipariş oluşturmalı
# Bu tarz kurallar İşletmenin işleyişini gösteren mantık sürecini ifade eder.

#%% Entity Relationship Diagram(ER diagram)
# Management studio da "database diagram" ile görselleştirebiliyorduk.
# Farklı görselleştirme yaklaşımları var ona bakacağız

# Entity: Nesnelerdir. Sürekli değişmeyen ve varlık olarak ifade edebileceğimiz şeylerdir
# .. İnsan, Araba, Öğretmen, Sınıf olabilir

# Relation: Nesneler arasındaki ilişki
# Bir öğretmen hangi sınıflara derse giriyor, öğretmen için entity, sınıf için entity
# .. ve bunlar arasındaki ilişki relationshiptir

# NOT: Diagramda --> Entity-Relationship modelinde entityler dikdörtgen içinde, relationshipler "karo(kartı)" şeklinde
# .. ifade edilir.(Farklı varyasyonları da olabilir)

# Attribute: Entity ye ait özellikler. Teacher ın kendine özgü özellikleri , Id, Name, Subject, Department vs
# .. Dept için dept_id, dept_name vs gibi.(entity attribute)
# Relationshiplerin de attributeları olabilir. Örneğin: ilişkinin başladığı tarih
# .. öğretmen bu departmanda çalışıyor mu hala çalışmıyor mu, sadece ilişkiye özgü bilgileride
# .. relationshipslere tanımlayabiliriz

# ÖRNEK : writer, novel, consumer : entitiler,  creates ve buys: relationship
# Bunlar 5 adet tablo. Bunlar arasındaki ilişkiyi sağlayan primary key ve foreign keyler
"""
writer --> creates --> novel 
                        |                        
     consumer  <---   buys 
"""

# Relationship: Weak ve Strong olabilir. 
# Relationship türleri; Burası önemli
"""
# 1:1     # 1 öğretmen sadece 1 departmanda çalışabilir. 
# 1:M     # 1 departmanda birden fazla öğretmen olabilir
# M:N      
# Unary   # Şemada aradaki bağlantı dolanıp(bir dikdörtgen oluşturuyordu) aynı tabloya dönüyordu. Bu o. ÖRNEK: staff_id, staff name,
# .. manager_id .. Hangi staff name in manager ı kim mesela 3(manager_id deki), son bu 3 e bakıyorum tekrar staff_id den bulup sonra 
# .. onun staff name ine bakıyorum ve manager ın ismini görmüş oluyorum. Yani hangi staff ın manager ı kim böyle dönüşlü yapılar unary.
# Ternary
"""

# Örneğin product ve brand tablosu
# brand tablosunda brand 1 defa geçer ama productta, brand 1 den fazla olabilir
# 1 product ın sadece 1 brand i olabilir ama 1 brandin bir çok product ı olabilir
# category-product : Her 1 ürün 1 kategoriye sahip olabilir. 1 kategori 1 den çok ürün içerebilir


# ERD Notations
# 2 çeşit notation kullanılıyor
# 1.Chen's notation 2.Crow's foot notation
# Biz ikinciyi(Crow's foot notation) kullanacağız
# Bağlantılarda şekil olarak; karga ayağı, hiç olamaz ya da en fazla 1 tane olabilirvs vs.
# ..  Crow's foot u bu diagramdaki işaretler gibi düşünebiliriz
# Örnek verelim
# Karga ayağı ve tek çizgi: Bağlı olduğu tablo Loan olsun. Book dan uzanarak gelmiş olsun.
# ... Loan dan book a da iki çizgi(||) var. Yani;
"""
   LOAN Ǝ-|  --------- || Book 
"""
# Ǝ-| : Her bir ödünç alma işleminde sadece 1 tane kitap ödünç alınabilir
# .. ve bir kitap birden fazla kere ödünç alınabilir
# NOT: Bu karga ayağı bir business rule dur. Veri tabanı buna uygun yapılmışsa sistem bu şekilde
# .. kitap alışverişine müsaade eder. Buna uygun yapılmamışsa etmez-hata verir. Bu yüzden
# .. veritabanını buna uygun oluşturulması çok önemli.

# NOT: KARGA AYAĞI : -E  YA DA  Ǝ-
"""
# Relationship

Student  -----(enrols)--- university

# Bu ikisi arasında ilişki var diyoruz
"""
############
"""
# One

Student | ------(has)------- | Student ID Number

# NOT: Student ID Number burada bir entity. Business rule a göre bunu entity yapmışlar
# Burada 1'e 1 ilişki . # Her bir öğrencinin 1 tane ID si vardır ve o id başka bir öğrencinin olamaz
"""
############
"""
# Many to many 
Student Ǝ-| -----(attends)----- |-E  Class

# Bir öğrenci birden fazla sınıftaki derse girebilir.
# O sınıfta birden fazla öğrenci olabilir
"""
############
"""
# One and ONLY One ( ------ || )
Student || ------(uses)------- || Chair
# Bir öğrencinin (en az) bir sandalyesi olmak zorunda, her bir sandalyenin de (en eaz) bir öğrencisi olmak zorunda
"""
############
"""
# Zeros or One ( ------ O| )
Student || ------(has)------- O| Chair 
"""
############
"""
# One or Many ( ------ |-E )
Instructor || ------(Teaches)------- |-E Class
"""
############
"""
# Zero or Many ( ------ O-E)
Classroom || ------(has)------- O-E Chair
"""


# How to Draw ER diagrams
# a.identify all entities
    # İlk olarak hangi entity lerin olacağını belirlemeliyiz(Öğrenci, Sınıf vs)
    # Öğrenci numarası entity mi olacak, attribute mu olacak vs
# b.identify relationshios
    # Hangi entitiler arasında ilişki olacak. Bu ilişkileri belirledikten sonra bu ilişkilerin
    # .. türlerini belirlemek gerekecek
# c.add attributes
    # Entity mi ifade eden hangi attribute lar olabilir. Bu attributelar sizin sorgulama
    # .. yapmanızı veya tablodaki raporların zengin olmasını sağlar

# Temel sıralama bu yukarıdaki şekilde

# CONSTRAINTS
# İki tablo arasındaki ilişkileri sağlayan yapılardır
# sale.orders tablosuna baktığımızda 1 primary key(order_id)  var, 3 foreign key(customer_id, store_id, staff_id)
# sale.orders(order tablom ile) customer_id(customer tablom) arasında bir relation var burada değil mi
# .. buradaki orders(sale) bir relationshiptir, bir entity değildir ama customer(sale) bir entitidir
# .. ya da customer(sale) ile product(product) arasındaki ilişkiyi order(sale) ve order_item(sale) tablosu
# .. ile sağlıyoruz diagrama bakarsak. Bu yapıyı sağlamaya çalıştığımız contraintleri foreign key lerle tanımlıyoruz

# %% C.Normalization
# Bazı kriterleri izleyerek normalizasyon yapacağız.
# Normalization fazları var.Biz 1. , 2. ve 3. fazları göstereceğiz bu derste

# SampleRetail da bir çok tablo vardı. Bunların hepsinin tek bir excel de tutulduğunu düşünelim
# 1. satırda yazmış olduğum müşteri bilgilerini yazıyorum çünkü müşteri bir ürün alıyor
# .. Müşteri tekrar ürün alırsa 2. satırda da tekrar o bilgileri yazmam gerekiyor vs vs
# .. Sonuçta bu veri structural olsa bile verinin analizini yapamayacağız.
# .. Çünkü ürünün adı değişti mesela. Bu ürün sipariş verildiği her satırı tek tek değiştirmemiz gerekiyor
# .. veya yeni bir ürün eklemek istedinizde, silme işleminde aynı problemler ortaya çıkacak
# Yani bunu mantıki tablolara bölmemiz lazım buna normalization diyoruz(denormalizeyi-normalize yapacağız)
# Normalization hali ile tabloları oluşturmamız lazım

# Anomally(Kuraldışılık/Aykırılık): Kuraldışı şeylerin önüne geçmeye çalışıyoruz biz normalleştirirken
# .. O yüzden bu anomalilere dikkat etmeliyiz 
# 1.Insertion Anomally   : Veri girerken olan anomalyler
# 2.Update Anomally      : Farklı satırlarda Bir ülke için farklı yüzölçümü görülmesi gibi
# .. Bu ülke ismini tek bir satırda ifade etmem lazım
# 3.Deletion Anomally    : örneğin üstteki ülke için 2 satırdan birini sildik diyelim. Ama doğru olanı mı sildik?

# How to Avoid Anomalies
# 1.Bir takım normalize olan tablolar create edeceğiz
# 2.Bazı functional dependency ler tanımlayacağız

# Normal Forms
# First normal form
    # 1.En az 1 tane primary key olmalı 
    # 2.Primary key dışındaki hücrelerde hep tek bir değer olmalı(Yani hücrede sadece tek bir tel no olmalı)
    # 3.Tekrarlayan satır olmamalı. Yani
        # örn: 63214512512   Zehra   Tekin    05051112233/05412221122
        #      63214512512   Zehra   Tekin    05051112233/05412221122
        # Bu tekrarlamış, bunu şöyle yapmalıyız farklı tabloda;
             # 05051112233   63214512512   Zehra   Tekin   
             # 05412221122   63214512512   Zehra   Tekin
             # 05433333311   21451251263   Cenk   Zorlu
             # Yani telno primary key oldu, tekrarlayan satır sorununu çözdük. primary key oluştu ve
             # .. her hücrede tek bir değer oldu
    ##### Bunları sağladıysanız 1. faz normalleştirmeyi yapmış oluyoruz
# Second normal form
    # NOT: Composite PK: 2 sütunun bir araya gelerek primary key oluşturması demek
    # 1.Primary key i ifade eden 1 den fazla sütun varsa, yani tek bir sütunla primary key yapamıyorum
    # .. primary key dışındaki bütün değerler bu 2 adet PK ya full bağımlı olmalı partial bağımlı olmamalı
    # .. yani non-key olan bir sütun primary keylerden herhangi biri ile ifade ediliyorsa bu "partial" dependency
    # .. bunu istemiyoruz. Böyle olursa neden 2 primary key var o zaman. Böyle olursa "partial" bağımlı olan
    # .. non-key i ve bağlı olduğu primary keylerden birini(bu aldığımız PK alındığı tablodada olacak diğer tablodada olacak)
    # .. başka bir tabloya almamız gerekiyor.
    ##### Yani sağlamamız gereken 2.fazda şey non-key bir sütunun ancak 2 PK bir araya gelerek o non-key i identify etmesi gerekiyor
    ##### ... Yani "Partial dependency" OLMAMASI gerekiyor
    ##### Primary key 1 tane ise otomatik 2. faz sağlanmış oluyor. Yani;
    ##### ... Eğer composite PK yapmamızı gerektiren bir durum yoksa 2. faz sağlanmış sayıyoruz
    ##### ... Tek bir primary key olsaydı ve non-key attribute o primary key ile ifade edilemiyor olsaydı yine
    ##### ... o non-key(sadece non-key i) i başka bir tabloya almam gerekirdi Yukarda satır 279 ve 280 de
    ##### ... telno tek başına zehra tekin i identify edemiyor. yani telno1 de zehra tekin, telno2 de zehra tekin
    ##### ... telnolar , isimleri identify edemiyor o yüzden isimler(isim ve soyisim) başka bir tabloda tutacağım
    ##### ... peki isim ve soyismi identify i ne olacak?? TCkimlikno identify edebiliyor. O yüzden tckno primary key,
    ##### ... isim ve soyisim non-key olacak şekilde başka tabloya alacağız
        ########### YANI SONUÇTA FULLY DEPENDENT OLMAYANLARI BAŞKA TABLOYA TAŞIYORUM
# Third normal form
    # 1.Primary key olmayan bütün değerlerin tamamen bağımsız olması yani;(Transitivity Dependency)
    # Transitivity Dependency.: bir non key attribute' un başka bir non key attribute' a bağımlı olmaması 
    # Bir müşteri tablosunda, primary key var(Customer_id), bi de diğer alanlar,
    # .. Bu diğer alanlar tamamen o müşteri ile alakalı olacak.
    # Bunları sağladıysanız 3. faz normalleştirmeyi yapmış oluyoruz

# Hoca: excel tablosu gönderiyorum(Normalization (library example)). Bunu beraber normalization yapacağız
# 2 çalışma sayfamız var denormalize ve normalize. Biz denormalizeden normalize haline getireceğiz

# Denormalize de Hepsi üstte tek bir tabloda
# Normalizede ayrı ayrı tablolarda

# Notları okuyacağız burada yeterli ya da SQL-2 dosyasında excel in açıklaması var

# DIKKAT: NOT: excelde -- normalize tablosunda satır 16 dan 23 e kadar olan "kitap_id" ile başlayan
# .. kısımda son satır yanlış onu sileceğiz. Çünkü ölü canlara yazar_id 2, ama en alt satırda 3
# .. ya sileceğiz ya da son satırı 2 yapacağız. Hoca en son son satırda yazar_id yi 2 yaptı

#################################################### END #################################################

