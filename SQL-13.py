#%% SQL-13. ders_20.06.2022(session-12)

#%% DATABASE INDEX

# Bir tabloda belli alanlara yapılan sorgular daha fazla ise
# .. ( Mesela: Kişi tablosunda sürekli isim üzerinden sotgu yapılıyor)
# .. Bu alanlara index atıyorsunuz. Bize fayda sağlıyor
# .. Indexler database seviyesinde oluyor. Yani DB deki bütün sütunlara index atalım diyemiyoruz
# NOT: Primary key ler ve foreign key ler de birer indextir aslında
# Management studioda bir sorgu yazdıktan sonra bu sorgu ne kadar sürüyor bunun için bir yapı sunuyor
# .. Bu bilgiye göre tablo ya da sorgularınızı değiştirebilirsiniz

# Burada 2 temel terim var. SCAN, SEEK
# Scan : SQL server sorguya bakıp bu kriter hangi satırlarda var ona bakıyor. Yani Full scan yapıyor.
# .. Bu yavaş metodtur ama her zaman doğru sonuç getirir
# Seek : Indexleri koyduktan sonra dict mantığıyla ilgili yeri bulur
# .. Index seek : 1.Clustered 2.Non-clustered
# a.Clustered Index: Belirli bir sütun üzerinde oluşturmuş olduğunuz cluster indexte SQL o sorgusunda
# .. o alana nerede ise o alana(kümeye) gidiyor hızlıca buluyor. Her bir tabloda tek bir clustered index
# .. olabiliyor. Çünkü sıralama belli bir sütuna göre yapıldıysa, diğer sütunlar o sıralanan sütuna göre 
# .. sıraya gireceği için tek bir clustered index oluyor. (B-tree mantığıyla çalışır)
"""
-- Örnek kod
-- CREATE CLUSTERED INDEX index_name ON schema_name.table_name (column_list);
-- Bunu çalıştırınca bir "VIEW" mantığıyla DB de bir nesne oluşuyor
"""
# b.Non-Clustered Index: Bir tabloda clustered index oluşturdunuz. Sonra farklı alanlara da index oluşturmak istiyorsunuz
# .. Bunlar non-clustered indexler olacaktır. Birden fazla tabloda non-clustered index oluşturulabiliyor ve 2 den fazla
# .. sütun üzerinde non-clustered index oluşturulabiliyor.(B-tree yapısı burada da geçerli)

# ADVANTAGES AND DISADVANTAGES
# ADVANTAGE    : 1.Hız, 2.sıralama 3.Unique indexes guarantee
# DISADVANTAGES: 1.INSERT, UPDATE and DELETE becomes slower, 2.Disk alanında yer kaplar

"""
--önce tablonun çatısını oluşturuyoruz.
create table website_visitor 
(
visitor_id int,
ad varchar(50),
soyad varchar(50),
phone_number bigint,
city varchar(50)
);

-- veri insert edelim while döngüsünde 1 den 200000 e kadar
DECLARE @i int = 1
DECLARE @RAND AS INT
WHILE @i<200000
BEGIN
	SET @RAND = RAND()*81
	INSERT website_visitor
		SELECT @i , 'visitor_name' + cast (@i as varchar(20)), 'visitor_surname' + cast (@i as varchar(20)),
		5326559632 + @i, 'city' + cast(@RAND as varchar(2))
	SET @i +=1
END;

-- Tabloyu kontrol edelim
SELECT top 10*
FROM
website_visitor

-- indexleri oluşturdunuz diyelim. Ama zaman içinde tabloda değişiklikler oldu diyelim.
-- SQL server sorgular arasında yönlendirme yapabilir. Yönlendirme yapabilmesi için bu istatistikleri kullanır
-- Biz bu istatistikleri kapatıp açabiliyoruz. Biz bu istatistikleri açalım
--İstatistikleri (Process ve time) açıyoruz, bunu açmak zorunda değilsiniz sadece yapılan işlemlerin detayını görmek için açtık.
SET STATISTICS IO on
SET STATISTICS TIME on

-- basit bir sorgu yapalım.
select * from website_visitor where visitor_id = 100 -- Burada 200000 satırı taradı

-- MS-SQL server da sorgumuzu seçip Execute ın sağında "V" işareti var onunda sağındakine(execution plan) tıklayalım
-- Çıktıda bazı şeyler geldi onların üzerine mouse la geldiğimizde bilgiler görünüyor
-- Select Coat: .. 
-- Table scan: Kullanmış olduğu yöntem. Bu ekranda en üstte. (Cluster yapınca burası "Clustered Index seek" olacak)
-- .. "Estimated number of rows to be read-->199999",
-- .. "Estimated number of execution -- 1" 
-- .. vs vs
-- 2 sorguyu karşılaştırmak için bunu kullanabilirsiniz
"""

#%% Dersin 2. bölümü

# Tabloda index oluşturalım
"""
Create CLUSTERED INDEX CLS_INX_1 ON website_visitor (visitor_id);
-- CLS_INX_1          : Index adı. NOT: Index adı DB içinde unique olmalı
-- ON website_visitor : website_visitor tablosu üzerinde tanımlandı
-- (visitor_id)       : Hangi alana uygulanacağı
-- Object Explorer da -- > tables - dbo.website_visitor -- > Indexes -- > CLS_INX_1(Clustered) ... Oluşmuş

-- Indexi attık artık SQL server visitor ID lerin nerede olduğunu biliyor. Artık sorgu daha hızlı gelecektir
select * from website_visitor where visitor_id = 100 -- Burada 200000 ın hepsini okumadı
-- sorguyu seçip yine "execution plan" a tıklayalım. Çıktıda "Clustered_Index seek" geldi
-- Not: Eğer tablolar çok büyükse mutlaka index atmamız gerekiyor.

-- visitor_id de index var şu an tekrar bir index oluşturursak bu artık clustered index olmayacak bu non-clustered index olacak
select ad from website_visitor where ad = 'visitor_name17'; -- 200000 satırı okudu yine
-- "execution plan"a bakalım
-- Peki bu alana index nasıl atacağız(Non-cluster)
CREATE NONCLUSTERED INDEX ix_NoN_CLS_1 ON website_visitor (ad);
-- "execution plan"a bakalım. Index seek. Artık en alttaki "leaf" leri okumak zrounda değil(B-tree de)
-- .. index içerisindeki ismi bulmaya çalışıyor. Sonra sonucu getiriyor.
"""
# --------------------------------------
"""
-- İsim ve soyisme beraber index atalım.(Aynı isim soyisme ait başka bir kişi olmadığı için)
Create unique NONCLUSTERED INDEX ix_NoN_CLS_2 ON website_visitor (ad) include (soyad)
-- Artık isim ve soyisme beraber gönderilen planda ne olacak bakalım 
select ad, soyad from website_visitor where ad = 'visitor_name17';
-- "execution plan" a göre indexe göre arama yaptı. Extra isim soyisim üzerinde arama yapmadı
"""
# --------------------------------------
"""
-- clustered index (visitor_id)
-- non-clustered index (ad)
-- non-clustered index (ad) include (soyad)
-- Üsttekileri yaptık. Peki sadece soyadı üzerinden sorgu yapsaydı
select ad, soyad from website_visitor where soyad = 'visitor_name17'; -- çıktı yok ama execution plana bakmak için böyle yazdık
-- execution plan "Index scan" yani tablonun hepsini kontrol ediyor Yani "index seek" yapmadı
"""

#%% Dersin 3. bölümü

# Python üzerinden SQL server a bağlanma
# ipynb. dosyası üzerinde notlar var











































