#%% SQL-10. ders_15.06.2022(session-9)


# Dersin 1. bölümü
#%% WINDOW FUNCTIONS
# 3 gün sürecek
# Hem daha az satır sorgu hem de verideki detayı kaybetmiyoruz

# CONTENT
# Window Functions(WF) vs GROUP BY
# Types of WF
# WF Syntax and Keywords
# Window frames      -- Çok önemli
# How to Apply WF

##################
# 1.GROUP BY vs WF
# GROUP BY  aggregate fonksiyon ile tek satır sonuç döndürüyordu.
# WF Aynı group by mantığında çalışıyor ama satır sayısında azalma olmuyor
# Group by biraz yavaş, WF daha hızlıdır(Genelde)

"""
                                    Group by      Window Functions      
# Distinct                          necessity      optional
# Aggregation                       necessity      optional
# Ordering                          invalid         valid
# Performance                       shower          faster
# Dependency on selected Field      dependent      independent

Distinct: Group by da distinct sonuç gelir, WF de bu oladabilir olmayadabilir
Aggregation : Aggregate kullanmak gerekir group by da, WF de bu oladabilir olmayadabilir çünkü aggregare haricinde bir çok fonksiyonu vardır 
Ordering : Group by içinde kullanılmıyor. Bir grup belirliyorsunuz. TAbloda birden fazla sınıf olsun
 .. bu tabloda sınıfa göre gruplama yaparsanız öğrencilerin notları arasında ortalama değişmez group by da
 .. WF de order by gerekiyor genelde. Belirlediğiniz grubun ortalamasına göre farklı sonuçlar döndürüyor WF

Performance : Group by biraz yavaş, WF daha hızlıdır(Genelde)

Dependency on selected Field: Group by yaparken bilgilerin seçilen alana bağlıdır. Bazı bilgiler kaybolur çıktıda
.. WF de bu bağımsızdır

"""

# GROUP BY: Group by yaptıktan sonra fonksiyon unique belirliyor grupları ve çıktı veriyor
# WF: Grupları kendiniz manuel tanımlayabiliyorsunuz. Bu her bir grup bize bir Frame(window) i gösteriyor

"""
-- Şimdi group by ve WF kullanarak bir örnek yapalım
-- Soru: Her bir ürünün toplam stok miktarını hesaplayın
---------- group by ; 
select product_id, Sum(quantity) from product.stock
group by product_id
order by 1

----------- WF;
-- Önce bir stock tablomuza bakalım
select * from product.stock
order by product_id

-- Yeni bir satır ekleyeceğiz şimdi
-- 1 numaraları ürünün bütün satırlardaki toplamını yazdırmak istiyorum
select *, sum(quantity) over(partition by product_id) sumWF
from product.stock
order by product_id

--- sum(quantity) over(partition by product_id) sumWF : her bir product_id için quantity toplamını al ve sumWF de yazdır

--- group by ile aynı sonuç istediği için distinct atacağız. distinct i product_id ye atacağız
select	distinct product_id, sum(quantity) over(partition by product_id) sumWF
from	product.stock
order by product_id

-- ÖNEMLİ NOT: Where şartına yazacağınız şart WF hesaplanmadan önce uygulanır
"""
###############
"""
-- Soru: markalara göre ortalama ürün fiyatlarını group by ve WF ile yapalım
----------- group by;
select brand_id, avg(list_price)
from product.product
group by brand_id 

------------ WF;
select brand_id, avg(list_price) over(partition by brand_id) as avg_price
from product.product
-- 520 rows

--  group by ile aynı çıktı gelmesi için distinct ekleyelim
select distinct brand_id, avg(list_price) over(partition by brand_id) as avg_price
from product.product
-- 40 rows
"""
###############
"""
-- 2 tane WF kullanalım
-- Soru: brand_id ye göre her bir brand_id de kaç ürün var ve her bir brand id ye göre en yüksek fiyatlı ürün
select	*,
		count(*) over(partition by brand_id) CountOfProduct,
		max(list_price) over(partition by brand_id) MaxListPrice
from	product.product
order by brand_id, product_id
"""

#%% Dersin 2. bölümü

"""
--  WF ile oluşturduğunu kolonlar birbirinden bağımsız hesaplanır.
-- Dolayısıyla aynı select bloğu içinde farklı partitionlar tanımlayarak yeni kolonlar oluşturabiliriz
-- group by lı sorgularda tek bir partition vardır(Select den sonra yazılan aggregate fonksiyonlar tek bir partition dır)
-- WF de sütunlar arasında partitionlar farklı olabilir

--Soru: WF ile her bir markadan kaçar tane ürün var ve her bir kategory içindeki toplam ürün sayısını bulalım

select	product_id, brand_id, category_id, model_year,
		count(*) over(partition by brand_id) CountOfProductinBrand,
		count(*) over(partition by category_id) CountOfProductinCategory
from	product.product
order by brand_id, product_id, model_year

-- 520 rows
-- brand_id    si 1 olandan toplam 41 ürün varmış, vs vs
-- category_id si 1 olandan toplam 40 ürün varmış, 4 numaralı kategoriden 283 tane ürün varmış vs vs
-- order by ile sıralamayı değiştirip ona göre çıktımızı istediğimiz sıralamada getirebiliriz
-- order by ile sonucu daha rahat gözlemliyoruz. O yüzden order by ile kullanmamız daha iyi olacaktır

-- NOT: Burada distinct yapabilir miyiz? Sonuç değişmez Çünkü product_id ler unique zaten
-- .. o yüzden product_id select bloğunda durduğu sürece distinct işe yaramayacaktır
-- .. product_id yi silip yaparsam distinct row sayısı azalacaktır. Çünkü çoklayan satırlar varolacak.
"""
##################
# 2.TYPES of WF
# a.Aggregate Functions --- Avg, min, ...
# b.Navigation Funtions --- Partition içerisinden gezinerek yaptığımız 
# c.Numbering Functions --- Partition lar içerisinde belirlediğimiz sıralama ile

##################
# 3.TYPES of WF
# Syntax and Keywords
# Select(columns) FUNCTION() OVER(PARTITION BY ... ORDER BY ... WINDOW FRAME) from table1;
# Hesaplayacağımız fonksiyonda sıralama önemliyse partition içinde order by yapıyoruz
"""
-- örnek kod
SELECT *, avg(time) over (partition by id order by date rows between 1 preciding and current row) as avg_time from time_of_sales

-- rows between 1 preciding and current row : 1 önceki satırla içinde bulunduğu satır ortalamasını al
"""

##################
# 4.Window frames 
# Verinin tamamı bir partition olsun sonra biz bunu farklı partition lara bölüyoruz sonra da
# .. bi basamak sonra satırlar arasındaki ilişkiye window frame tanımlıyoruz. Asıl konu burada dönüyor.
# .. belirlediğimiz frame üzerinde fonksiyonumuz çalışıyor. Bunun sınırlarını değiştirebiliyorum
# .. Örneklerde daha net oturacak.
# current row: işlem yapılan satır olsun mesela
# partition başından itibaren current row a kadar olan satır bu satır benim frame im olsun diyebilirim(current row dahil) -- unbounded(kümülatif toplam)
# partition  current row dan itibaren sona kadar olan satır bu satır benim frame im olsun diyebilirim .. 
# N Preciding, M following Current row dan başlarsam; 3 önceki satırdan başlayıp 5 sonraki satıra kadar git diyebilirim. Toplam 9 satırım olacaktır

##################
# 5. How to Apply WF
"""
/*
örnek

id      date       time
1     2019-07-05    22
1     2019-04-15    26
2     2019-02-06    28
1     2019-01-02    30
2     2019-08-30    20
2     2019-03-09    22

PARTITION BY id                ---> ORDER by             -- avg(time)(ROWS BETWEEN 1 PRECIDING AND CURRENT ROW)
id      date        time      id  date         time     id        date    time       avg_time
1     2019-07-05    22        1   2019-01-02    30       1   2019-01-02    30          30
1     2019-04-15    26        1   2019-04-15    26       1   2019-04-15    26          28
1     2019-01-02    30        1   2019-07-05    22       1   2019-07-05    22          24
                                                         2   2019-02-06    28          28
id      date        time      id  date         time      2   2019-03-09    22          25
2     2019-02-06    28         2  2019-02-06   28        2   2019-08-30    20          21
2     2019-08-30    20         2  2019-03-09   22
2     2019-03-09    22         2  2019-08-30   20

*/
--- Çalışacağınız yerde raporlama yapılıyorsa bu WF konusunu çok fazla kullanıyorsunuz
"""
#############
"""
-- Sürekli kullanılabilecek bir sorgu göstereceğiz WF ile alakalı
-- Windows frame i anlamak için birkaç örnek:
-- Herbir satırda işlem yapılacak olan frame in büyüklüğünü (satır sayısını) tespit edip window frame in nasıl oluştuğunu aşağıdaki sorgu sonucuna göre konuşalım.

SELECT	category_id, product_id,
		COUNT(*) OVER() NOTHING,
		COUNT(*) OVER(PARTITION BY category_id) countofprod_by_cat,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id) countofprod_by_cat_2,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) prev_with_current,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) current_with_following,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) whole_rows,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) specified_columns_1,
		COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN 2 PRECEDING AND 3 FOLLOWING) specified_columns_2
FROM	product.product
ORDER BY category_id, product_id

--Detay olarak category_id, product_id yi aldık sadece. 8 tane de WF yazdık
-- farklı frame yapıları tanımlandı. her bir frame de kaç satır geliyor görmek için bu örneği kullanıyoruz
-- sorgunun tümünü çalıştırınca -520 rows. Herhangi bir satırda herhangi bir filtreleme yapmadık demek bu
-- 1 WF: OVER() NOTHING : Partition ınımız tablomuzun tamamıdır ve tek bir partition vardır. Büyüklüğü? Tablomuzun tamamıdır. Yani 520 rows
-- 2 WF: COUNT(*) OVER(PARTITION BY category_id) countofprod_by_cat : her bir category_id için farklı bir değer hesaplanacak
-- 3 WF: COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id) countofprod_by_cat_2, : order by eklenmiş. ürünlerin sıralaması önemli değil normalde 
-- .. ama order by tanımladığımız için Window frame imiz değişiyor.
-- .. yani Window frame tanımlamazsak partition başından current row a kadar olan bizim window frame imizdir. (örn: 10. satır için ilk satırdan 10 a kadar gidiyor hepsini count yapıyor vs vs)
-- 4 WF:COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) prev_with_current, :
-- ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW: Bu default değer olduğu için bir üstteki ile aynı çıktı geldi. Açıklama için bir altın açıklamasına bakınca onun tersi
-- diye mantık kurup anlayabiliriz
-- 5 WF:COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING) current_with_following, :
-- .. üsttekinin tam tersi bir window frame var (yukarda unb-current), burada (current-unb fol)
-- .. BETWEEN CURRENT ROW AND UNBOUNDED FOLLOWING: Current rowdan(parition ımızın) partition ımın sonuna kadar(ilk satır için partition ın tamamıdır yani 40)
-- .. 2. satırdaonun 1 eksiği vs (yani birinci partition da 40 yazdırdı, sonra 39, sonra 37 vs vs.)
-- 6 WF:COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) whole_rows, :
-- .. ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) whole_rows : partition ın en başı ve en sonu. Partition da hangi satırda olursam olayım daima partition ımın başı ve sonu
-- .. arasında işlem yap. O yüzden hepsi 40 geldi. 1 WF ile aynı sonucu üretti.
-- 7 WF:COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) specified_columns_1, : 
-- .. ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING : partition içerisinde 1 satır öne git ve 1 satır sonraya git( Toplamda 1 önceki current ve 1 sonrakini alıp 3 satır alıyor 
---.. NOT: Eğer 1 üst satır ya da 1 alt satır partition içerisinde değilse onu işleme alamıyoruz(1. satır için count(*)=2 dir(current ve sonraki toplam 2), 2. satır için 3, 3. satır için 3 vs , partition sonunda
-- .. yani mesela 40. satırda yine 2 gelmiş(1 önceki ve 1 current toplam 2))
-- 8 WF:COUNT(*) OVER(PARTITION BY category_id ORDER BY product_id ROWS BETWEEN 2 PRECEDING AND 3 FOLLOWING) specified_columns_2 :
-- .. Bu da üstteki ile aynı mantık ilk frame 4(1 current ve 3 following), 2. si 5(1 üst,1 current ve 3 following), 3. sü 6(2 satır üst,1 current ve 3 following)
"""

#%% Dersin 3. bölümü
# WF lerde aggregate functions
# Analytic Aggregate Functions :  min(), max(), avg(), count(), sum()

"""
-- Soru: Her bir kategorideki en ucuz ürünün fiyatı nedir? category_id ve "cheapest_by_cat"
select *, min(list_price) over(partition by category_id) cheapest_by_cat
from product.product

-- her kategorinin yanına o ürünün en ucuz fiyatını getirdi
-- distinct li sonuç istediği için distinct atalım
select	distinct category_id, min(list_price) over(partition by category_id) cheapest_by_cat
from	product.product
"""
####### 
"""
-- Soru: Product tablosnda kaç farklı product var. Toplam ürün sayısını WF ile yapınız
select distinct count(*) over() as num_of_product
from product.product

-- Tek bir satırlık sonuç istiyor. Toplam ürün sayısını istiyor
-- Farklı ürünü bulurken count(*) yapmamız yeterli çünkü product_id unique
-- her bir product için o sayı(520) tekrarlayacağı için distinct yazmalıyım
"""
#######
"""
-- Soru: How many differnt product in the order_item table? 520 tane ürünün kaç tanesini satmışım?
-- Bu soru diğer soruya göre biraz farklı
-- 1 ürün bu tabloda 1 den fazla tabloda geçebilir burada. product_id unique değil

select distinct product_id, count(*) over(partition by product_id) as num_of_order
from sale.order_item
-- 307 rows -- Bu tabloda 307 farklı ürün(product_id) varmış
-- Bu 307 sonucunu tek satırda istiyoruz.

-- group by ile bunu yapsaydık
select count(distinct product_id) UniqueProduct from sale.order_item

--- WF ile deneyelim
select count(distinct product_id) over() UniqueProduct from sale.order_item -- HATA. Bunu count içinde distinct olacaksa bunu group by ile yapabiliriz

-- ya da mesela select distinct product_id yi başka yerde tanımlayacağız
select distinct count(*) over()
from (select distinct product_id,  count(*) over(partition by product_id) as number_of_product
from sale.order_item) as a
"""
########

"""
-- Soru: Write a query that returns how mant products are in each order?
-- Her bir siparişte kaç farklı ürün olduğunu döndüren bir sorgu yazın? 

-- group by ile
select	order_id, count(distinct product_id) UniqueProduct,
		sum(quantity) TotalProduct
from	sale.order_item
group by order_id
-- o siparişte uniquer product sayısı ve toplam kalem sayısını getirdi
-- sum(quantity) TotalProduct: Mesela order_id 1 de toplam 5 farklı ürün var toplam 8 ürün var

-- WF ile
select distinct order_id, 
count(product_id) over(partition by order_id) Count_of_Uniqueproduct,
SUM(quantity) over (partition by order_id) Count_of_product
from sale.order_item
"""
########
"""
-- How many different product are in each brand in each category?
-- Herbir kategorideki herbir markada kaç farklı ürünün bulunduğu
select distinct category_id, brand_id,
 count(*) over(partition by brand_id, category_id) count_of_Product
from product.product

-- 1 numaraları kategoride 1 numaralı markaya ait 15 tane ürün varmış,
-- 4 numaraları kategoride 8 numaralı markaya ait 15 tane ürün varmış vs vs ...

-- brand isimlerini getirmek istersek üstteki sorguyu bir subquery olarak kullanabiliriz
select A.*, B.brand_name from 
(select distinct category_id, brand_id,
 count(*) over(partition by brand_id, category_id) count_of_Product
from product.product
 ) A, product.brand B
where A.brand_id = B.brand_id

--- join ile WF örneği- aynı sonucu alalım
select distinct category_id, A.brand_id,
count(*) over(partition by A.brand_id, A.category_id) count_of_Product,
B.brand_name
from product.product A, product.brand B
WHERE A.brand_id = B.brand_id
"""



































