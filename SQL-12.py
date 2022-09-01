#%% SQL-12. ders_18.06.2022(session-11)


#%% NUMBERING FUNCTIONS
# Sıralama ile partition lara bölme, kümülatif oranlar oluşturma, Numaralandırma vs

############ NUMBERING FUNCTIONS 1
# ROW_NUMBER : HEr bir partition içerisinde 1 den başlayıp artan bir sütun oluşuyor
# RANK : 1 den başlayarak Değerler arasında fark var ise sıralıyor. Aynı değerlere aynı rankı veriyor. (Örnekle daha iyi anlaşılacak)
# DENSE_RANK: Dense_rank e benziyor ancak --> (Örnekle daha iyi anlaşılacak)
    # aynı partition içinde; 
        # row_number: 1-2-3-4-5
        # Rank örnek: 1-2-2-2-5
        # DEnse_rank: 1-2-2-2-3    
"""
-- Row_Number()
--Soru: Her bir kategori içinde ürünlerin fiyat sıralamasını yapınız.
select product_id, category_id, list_price
from product.product

-- Partition içinde sıralama yaptı
----------------------------------
-- Rank() -- Dense_Rank()
select product_id, category_id, list_price,
ROW_NUMBER() over(partition by category_id order by list_price) RowNum,
RANK() over(partition by category_id order by list_price) [Rank],
DENSE_RANK() over(partition by category_id order by list_price) Dense_Rank
from product.product

-- satır 16 -- > rank:15,  dense_rank:16 çünkü list_price satır 14 ve 15 te aynı. Eğer satır 12,13,14,15 te 
-- list_price aynı olsaydı, satır 12,13,14,15 de rank:12 , dense_rank:12 olup, satır 16 da rank: 16, dense_rank : 13 olacaktı
-- NOT: RowNum : Buna "Camel type" isimlendirme deniyor
-- NOT: [Rank] : Köşeli parantez içinde yazdığım içindeki kelimeleri SQL server string ifade gibi algılar.
-- NOT: Dense_Rank: Pembe olarak çıkıyor. Çünkü bu SQL de bir fonksiyon ismi. Bunu değiştirmek önerilir
----------------------------------
-- Soru: Herbir model_yili içinde ürünlerin fiyat sıralamasını yapınız (artan fiyata göre 1'den başlayıp birer birer artacak)
-- row_number(), rank(), dense_rank()
SELECT product_id, model_year,list_price,
		ROW_NUMBER() OVER(PARTITION BY model_year ORDER BY list_price ASC) RowNum,
		RANK() OVER(PARTITION BY model_year ORDER BY list_price ASC) RankNum,
		DENSE_RANK() OVER(PARTITION BY model_year ORDER BY list_price ASC) DenseRankNum
FROM product.product;
"""

############ NUMBERING FUNCTIONS 2
# CUME_DIST()    : Kümülatif distribution = Row number/total rows. Kümülatif değerler getirecek ve son satır "1" olacak
# PERCENT_RANK() : Percent_rank = (row number -1) /(total rows -1)
# NTILE(N)       : Eşit sayıda kümelere bölme. Veri sıralandıktan sonra küme sayısını belirtip kümeleme yapıyoruz

"""
-- Soru: Write a query that returns the cumulative distribution of the list price in product table by brand.
-- product tablosundaki list price' ların kümülatif dağılımını marka kırılımında hesaplayınız
SELECT brand_id,list_price,
    ROUND(CUME_DIST() OVER(PARTITION BY brand_id ORDER BY list_price),3) as CUM_DIST
FROM product.product;

-- brand_id partition a göre ilk veri yüzde kaçlık dilime denk geliyorsa yazdı, 
-- ..partition bittiğinde, yani son değer 1 oldu
--  ROUND(x,3) --- virgülden sonra kaç basamak görmek istiyoruz: 3 basamak		
----------------------------------
-- Soru: Write a query that returns the relative standing of the list price in product table by brand.
SELECT brand_id,list_price,
    ROUND(CUME_DIST() OVER(PARTITION BY brand_id ORDER BY list_price),3) as CumDist,
    ROUND(PERCENT_RANK() OVER(PARTITION BY brand_id ORDER BY list_price),3) as PercentRank
FROM product.product;
----------------------------------
-- Yukarıdaki CumDist sütununu CUME_DIST fonksiyonu kullanmadan hesaplayınız
with tbl as (
	select	brand_id, list_price,
			count(*) over(partition by brand_id) TotalProductInBrand,
			row_number() over(partition by brand_id order by list_price) RowNum,
			rank() over(partition by brand_id order by list_price) RankNum
	from	product.product
)
select *,
	round(cast(RowNum as float) / TotalProductInBrand, 3) CumDistRowNum,
	round((1.0*RankNum / TotalProductInBrand), 3) CumDistRankNum
from tbl
-- WITH ile geçici tablo oluşturduk, sorgumuz daha sade gözüksün diye
-- Row_number la hesaplamak mı, Rank_number la hesaplamak mı daha doğru baktık. --
-- Tam istediğimiz sonuca ulaşamadık 2 si ile de. Hoca bakıp sonucu atacak
"""
# ----------------------- Farklı örnekler
"""
--Write a query that returns both of the followings:
--The average product price of orders.
--Average net amount.
--Aşağıdakilerin her ikisini de döndüren bir sorgu yazın:
--Siparişlerde yer alan ürünlerin liste fiyatlarının ortalaması
--Tüm siparişlerdeki ortalama net tutarı
SELECT DISTINCT order_id, 
AVG(list_price) OVER(PARTITION BY order_id) avg_price, 
AVG(list_price * quantity* (1-discount)) OVER() avg_net_amount
FROM sale.order_item

-- OVER() : Tablonun tamamı tek bir partition olmasını istediğimiz için partition yapmadık burada
-----------------------------------
-- Soru: --List orders for which the average product price is higher than the average net amount.
--Ortalama ürün fiyatının ortalama net tutardan yüksek olduğu siparişleri listeleyin.
select * from (SELECT DISTINCT order_id, 
cast(AVG(list_price) OVER(PARTITION BY order_id) as numeric(6,2)) AvgPrice, 
cast(AVG(list_price*quantity*(1-discount)) OVER() as numeric(6,2)) AvgNetPrice
FROM sale.order_item) A
where A.AvgPrice > A.AvgNetPrice
-------------------------------------------
-- Cumulative sorusu
-- Soru : Calculate the stores' weekly cumulative number of orders for 2018
SELECT A.store_id, A.store_name, B.order_date,
DATEPART(ISO_WEEK, B.order_date) WeekOfYear
FROM sale.store A, sale.orders B where A.store_id = B.store_id And Year(B.order_date)= '2018'
order by 1,3
-- Şimdi partition ım burada store_id ve week of year olacak
-- Yani store id ve Select bloğunda DATEPART(ISO_WEEK, B.order_date) fonksiyonun sonucundan dönene göre partition yapacağız
SELECT A.store_id, A.store_name, B.order_date,
DATEPART(ISO_WEEK, B.order_date) WeekOfYear,
COUNT(*) OVER(PARTITION BY A.store_id, DATEPART(ISO_WEEK, B.order_date)) weeks_order
FROM sale.store A, sale.orders B where A.store_id = B.store_id And Year(B.order_date)= '2018'
order by 1,3
-- Bir sonraki sütuna geçelim. Mağazanın kümülatif satış sayısı(haftalık)
select  a.store_id, a.store_name, -- b.order_date,
	datepart(ISO_WEEK, b.order_date) WeekOfYear,
	COUNT(*) OVER(PARTITION BY a.store_id, datepart(ISO_WEEK, b.order_date)) weeks_order,
	COUNT(*) OVER(PARTITION BY a.store_id ORDER BY datepart(ISO_WEEK, b.order_date)) cume_total_order
from sale.store A, sale.orders B
where a.store_id=b.store_id and year(order_date)='2018'
ORDER BY 1, 3
-- 1. haftada toplam 4 satış, ccum satış 4 , 2. hafta 6, cum satış 10 , 3. hafta 3, cum_satış 13 vs vs
-- Son olarak buna bir distinct atalım.
select distinct a.store_id, a.store_name, -- b.order_date,
	datepart(ISO_WEEK, b.order_date) WeekOfYear,
	COUNT(*) OVER(PARTITION BY a.store_id, datepart(ISO_WEEK, b.order_date)) weeks_order,
	COUNT(*) OVER(PARTITION BY a.store_id ORDER BY datepart(ISO_WEEK, b.order_date)) cume_total_order
from sale.store A, sale.orders B
where a.store_id=b.store_id and year(order_date)='2018'
ORDER BY 1, 3
-- Sonuç: Her bir satır o haftanın toplam satış sayısını gösteriyor
-------------------------------------------
-- Soru: Calculate 7-day moving average of the number of products sold between '2018-03-12' and '2018-04-12'
-- o günlük satış ve 1 önceki haftanın ortalama satış sayısı

--- Önce ihtiyacımız olanlara bakalım
select B.order_date, A.order_id, A.product_id, A.quantity
from sale.order_item A, sale.orders B
where A.order_id = B.order_id
-- Ayın 1 inde toplam 11 tane ürün satışmış, ayın 2 sinde toplam 2 ürün
-- günlük bazda kaç ürün satıldığını bilmem lazım
-- 7 gün geri ve ileri gidebileceğim ve birbiriyle kıyaslayabileceğim bir yapı olmalı
-- Bu veri setinden tek bir gün için toplam quantity yi görmem lazım onu 1 hafta öncesiyle katşılaştıracağız
-- Bunu da sorgum karışık olmasın diye WITH ile geçici tablo oluşturalım
with tbl as (
	select	B.order_date, sum(A.quantity) SumQuantity --A.order_id, A.product_id, A.quantity
	from	sale.order_item A, sale.orders B
	where	A.order_id = B.order_id
	group by B.order_date)

-- Son 7 gündeki hareketli ortalamayı hesaplayacağız. Bunu da o günden geriye 7 satır git
-- .. o değerlerin ortalamasını getir diyeceğiz. O günün yanına yazdıracağız
with tbl as (
	select	B.order_date, sum(A.quantity) SumQuantity --A.order_id, A.product_id, A.quantity
	from	sale.order_item A, sale.orders B
	where	A.order_id = B.order_id
	group by B.order_date
)
select	*,
	avg(SumQuantity) over(order by order_date rows between 6 preceding and current row) sales_moving_average_7
from	tbl
where	order_date between '2018-03-12' and '2018-04-12'
order by 1

-- partition yapmama gerek yok ancak frame belirlemem lazım(7 satırlık ortalama için)
-- between 6 preciding and current row : 6 satır geriye + 1 current row = 7 günlük 
-- Ortalamayı integer yerine float istersek cast(.. as float.. ) şeklinde yapabiliriz
-- Siparişi olmayan tarihler var. O zaman gerideki günleri sayamayacağız.
-- Eğer bu kayıp günler önemliyse, tariht tablosu oluşturmamız lazım
-- .. left joinle olmayan tarihleride ekleyelim sonra olmayan tarihlerin karşısına 0 yazıp sonra
-- .. üstteki sorgumuzla sonuca ulaşabiliriz
-- where bloğunda koşulu alıp ondan sonra filtreleme yapıyor burada
-- önce partition yapıp sonra filtrelemeyi yapacaksam . partitionlı sorguyu bir tabloya kaydedip
-- .. sonra where bloğu ekleyebilirim başka bir sorguda
-------------------------------
-- Soru: List customers whose have at least 2 consecutive orders are not shipped

-- NOT: Hoca kendisi gerçek hayatta çözdüğü bir problemin çözümünü atacak notlarda


