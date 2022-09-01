#%% SQL-11. ders_16.06.2022(session-10)

#%%
"""
-- How many different product are in each brand in each category?
-- group by ile
select category_id,brand_id,COUNT(product_id)
from product.product
group by category_id,brand_id
------------------------------------------------
-WF ile
select distinct category_id,brand_id,COUNT(product_id) OVER(PARTITION BY category_id,brand_id) cnt_prod
from product.product
"""

##########
# FIRST_VALUE FUNCTION
# Bir sütun için en üst satırda yer alan değeri getiriyor(Partition, WF ve koşullara göre)
"""
-- Örnek kod
Select A.customer_id, A.first_name, B.order_date,
FIRST_VALUE(order_date) OVER (ORDER BY B.Order_date) first_date from sale.customer A, sale.orders B 
WHERE A.customer_id = B.customer_id
"""
# ------------------------
"""
-- Soru: Write a query that returns most stocked product in each store
-- Sorunun ilk kısmını yapalım burada her bir store a göre en çok stoğu olan product_id ne buna bakacağım
Select store_id, product_id,
FIRST_VALUE(product_id) OVER(PARTITION BY store_id ORDER BY quantity DESC) most_stocked_prod
FROM product.stock
-- product_id nin ilk değerini alıp , quantity ye göre DESCENDING sıralamam gerekiyor. 
-- Çünkü azalan sıralamada en yüksekten düşüğe gidiyor. Yani first value dediğimde
-- bunun en üsttekini yani order by yaptığımız için maximum değerini aldı
-- store_id 1 karşısına gelen 30 numaralı ürün 30 tane varmış
-- store_id 2 karşısına gelen 64 numaralı ürün 30 tane varmış
-- most_stocked_prod --> first_value of product_id
-- Şimdi istediğimiz çıktıyı getirelim
Select distinct store_id, 
FIRST_VALUE(product_id) OVER(PARTITION BY store_id ORDER BY quantity DESC) most_stocked_prod
FROM product.stock
-- Elde etmek istediğimiz sonuç geldi
-------------------------
-- Üstteki sorguda En yüksek quantity ye sahip ürün ve miktarı
Select distinct store_id, 
FIRST_VALUE(product_id) OVER(PARTITION BY store_id ORDER BY quantity DESC) most_stocked_prod,
FIRST_VALUE(product_id) OVER(ORDER BY quantity DESC) MSP_W
FROM product.stock
"""

#%% Dersin 2. bölümü
"""
-- Soru: --Write a query that returns customers and their most valuable order with total amount of it.
-- Müşterilerin en yüksek miktara sahip değerlerini döndürün
select B.customer_id
from sale.order_item A, sale.orders B
WHERE A.order_id = B.order_id
--Şimdi.. En değerli siparişi nasıl bulabiliriz. müşteriler- siparişler ve net price larına bakacağım ve
-- her bir müşteri için en yükseğini bulacağım
SELECT	customer_id, B.order_id, SUM(quantity * list_price* (1-discount)) net_price
FROM	sale.order_item A, sale.orders B
WHERE	A.order_id = B.order_id
GROUP BY customer_id, B.order_id
ORDER BY 1,3 DESC;
-- net price ı her bir customer_id ve sipariş için bulmuş olduk
--customer_id 1 için en yüksek amoun 1038.5370, -- order_id 1555, 3 için, 6763.3454 -- order_id 1612

-- Devam edelim ve üsttekini bir alt sorguya alıp kaydedelim WITH ile
-- Sonra onu(WITH T1) i kullanarak istediğimiz sonuca ulaşalım
WITH T1 AS (
select customer_id, B.order_id, SUM(quantity*list_price*(1-discount)) net_price
from sale.order_item A, sale.orders B where A.order_id = B.order_id
Group by customer_id, B.order_id
)
Select distinct customer_id,
FIRST_VALUE(order_id) OVER(PARTITION BY customer_id ORDER BY net_price Desc) MV_order,
FIRST_VALUE(net_price) OVER(PARTITION BY customer_id ORDER BY net_price Desc) MV_order_NET_PRICE
from T1
-- En yüksek net price a sahip siparişi getirdik ve distinct yaptık
-- 2. partition da net price ı getireceğiz ve ilk satırdaki değeri alacağız
-- MV: most valuable
"""
# ---------------------------------------
"""
Soru: Write a query that returns first order date by month
Select distinct Year(order_date) Year, Month(order_date) Month,
FIRST_VALUE(order_date) 
OVER(PARTITION BY Year(order_date),Month(order_date) ORDER BY Year(order_date)) first_order_date 
from  sale.orders

-- FIRST_VALUE(order_date): Her bir ay bazında ilk order_date i istiyorduk
"""

#%% Dersin 3. bölümü

# LAST_VALUE
# Sıralanmış sütun değerleri içerisinden son değeri getiriyor
"""
-- Örnek kod
Select A.customer_id, A.first_name, B.order_date,
last_value(order_date) OVER (ORDER BY B.Order_date desc) last_date from sale.customer A, sale.orders B 
WHERE A.customer_id = B.customer_id

-- order_date ve last_date aynı değerler gelmiş. Çünkü default frame koşulunu kullandı
-- Her bir satır için bir önceki satırı hesaba kattı
-- 1. satır, önceki satır yok, kendisini aldı,
-- 2. satırda önceki satırı 1. satır, bunlardan last_valueyu alıyor yani 2 yi o yüzde
-- 3. ... 
--- O yüzden Rows between unboundend preciding and unbounded following demek lazım.
-- yani last_value kullanırken Window frame i ütteki şekilde kullanmalıyız
"""
# ------------------------------------------
"""
-- Store tablosunda en yüksek quantity ye sahip ürünü last_value ile getirmek istiyorum
-- Önce stock tablomuza bakalım tekrar
select * from product.stock order by 1,3 asc
-- Devam edelim
SELECT	DISTINCT store_id,
		LAST_VALUE(product_id) OVER (PARTITION BY store_id ORDER BY quantity ASC, product_id DESC ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) most_stocked_prod
FROM	product.stock
-------
SELECT	DISTINCT store_id,
		LAST_VALUE(product_id) OVER (PARTITION BY store_id ORDER BY quantity ASC, product_id DESC RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) most_stocked_prod
FROM	product.stock

-- order by da 2 tane sütun kullandık
-- NOT: range ile rows hemen hemen aynı işlemleri yapıyor
    -- rows : unbounded preciding/following gibi keyword lerle kullanıp staır sayısı belirtmek istiyorsanız kullanıyoruz
    -- range: yine keyword ler kullanılıyor ANCAK Manuel olarak satır sayısı belirtemiyorsunuz
"""

###########
# LAG() AND LEAD()
# LAG() : Her bir satır için kendisinden belirttiğimiz kadar önceki satır değerini getiriyor
        # Örneğin; order_date sütunundan 3 önceki değeri o değerin yanına getiriyoruz
        # default u 1 : Kendisinden 1 önceki satır değerini al
        # Null değer için bir şey yazdırmak istiyorsak, onu null un yerine yazdırabiliyoruz
"""
-- Örnek kod
SELECT order_date,
lag(order_date,2) OVER(ORDER BY order_date) previous_second_w_lag from sale.orders
"""
# LEAD() : lag ın tersi olarak sonraki satır ddeğerlerini alıyoruz
"""
-- Örnek kod
SELECT order_date,
lead(order_date,2) OVER(ORDER BY order_date) next_second_w_lead from sale.orders
"""
# ------------------------------
"""
-- Soru: Her bir staff için çalışanların aldığı siparişlerin 1 önceki sipariş tarihlerini yazdırın
SELECT	A.staff_id, B.first_name, B.last_name, A.order_id, A.order_date,
		LAG(order_date) OVER(PARTITION BY A.staff_id ORDER BY A.order_id) prev_order
FROM	sale.orders A, sale.staff B
WHERE	A.staff_id = B.staff_id

--Write a query that returns the order date of the one next sale of each staff (use the LEAD function)
SELECT	DISTINCT A.order_id, B.staff_id, B.first_name, B.last_name, order_date,
		LEAD(order_date, 1) OVER(PARTITION BY B.staff_id ORDER BY order_id) next_order_date
FROM	sale.orders A, sale.staff B
WHERE	A.staff_id = B.staff_id

-- Sütunları çektik
-- her bir siparişin kendisinden 1 önceki sipariş tarihini aldık
-- Örneğin ;3. siparişten bir önceki sipariş 9 , bunun tarihi 2018-01-05 sonra 3. satırda 12, 2018-01-06 nın yanına 2018-01-05 geldi
-- diğer satırlar aynı mantık. İlk sütundan önce sipariş olmadığı için NULL geldi
-- Not: order_id 20 numaralı sipariş için 1 önceki tarih aynı o yüzden order_by da A.order_date yerine
-- .. A.order_id ye göre yaparsak daha mantıklı olabilir. Çünkü order_date e göre sıralayınca önce order_id 19 u mu almalı yoksa 20 yi mi
-- .. gibi bir sorun oluşuyor. O yüzden order_id ye göre sıraladık

-- Eğer partition yapmasaydım order_id 1,2,3,4 diye gidecek ve staff ler farklı olacaktı
SELECT	A.staff_id, B.first_name, B.last_name, A.order_id, A.order_date,
		LAG(order_date) OVER(ORDER BY A.order_id) prev_order
FROM	sale.orders A, sale.staff B
WHERE	A.staff_id = B.staff_id
"""
