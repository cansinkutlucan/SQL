#%% SQL-9. ders_13.06.2022(session-8)


#%% 1.CORRELATED SUBQUERIES
# Çok yaygın kullanılır
# 2 fonksiyon var burada. 1.Exist 2.non-exist
# exist : tabloya bir sorgu atıyorusunuz sonra B tablosundan ya da yine A tablosunda bu kayıtların başka bir yerde bulunup
# .. bulunmadığına bakıyorsunuz. Bir alan çekmiyorsunuz oradan. Sadece var mı yok mu buna bakıyoruz. Bir check etme işlemi yani
# NOT exist : Tam tersi 2. tabloda olmama durumunu test ediyorsunuz

"""
-- EXIST
SElect * from sale.customer WHERE EXISTS(SELECT 1)

SELECT * from sale.customer A WHERE EXISTS (SELECT 1 FROM sale.orders B WHERE B.order_date > '2020-01-01' AND A.customer_id=B.customer_id)
-- Bana sadece 2020 ocak 1 den sonra sipariş vermiş olma "durumunu" göster
-- SELECT 1: Buradaki 1 in hiç bir anlamı yok. Buna takılmayalım
"""
##############
"""
-- NOT EXIST
SElect * from sale.customer WHERE NOT EXISTS(SELECT 1)

SELECT * from sale.customer A WHERE NOT EXISTS (SELECT 1 FROM sale.orders B WHERE B.order_date > '2020-01-01' AND A.customer_id=B.customer_id)
# Bana sadece 2020 ocak 1 den sonra sipariş yapmış olmama "durumunu" göster
# Soru: Bu sorguda diyelim biri yeni kaydedilmiş ve siparişi olmamış. BU sorgu sonucunda bu müşteri gelir mi gelmez mi ?
# ...Kriter şu burada: Customer tablosuna gidiyor her bir satır için customer_id 1 sonra order tablosuna gidiyor orders ı varsa alıyor yoksa almıyor
# ... inner query içinde varsa o kişiyi alıyor yoksa eliyor. Yani gelmesi lazım
"""

"""
Soru: Apple - Pre-Owned iPad 3 - 32GB - White ürünün hiç sipariş verilmediği eyaletleri bulunuz.
Eyalet müşterilerin ikamet adreslerinden alınacaktır.

Select * from product.product WHERE product_name = 'Apple - Pre-Owned iPad 3 - 32GB - White'

-- Bu ürünün hangi siparişlerde verildiğini bir sorgulayayım sonra eyalet kısmına geçiş yapalımö

select	distinct C.state
from	product.product P,
		sale.order_item I,
		sale.orders O,
		sale.customer C
where	P.product_name = 'Apple - Pre-Owned iPad 3 - 32GB - White' and
		P.product_id = I.product_id and
		I.order_id = O.order_id and
		O.customer_id = C.customer_id
;

-- Şimdi bana öyle bir eyalet getir ki o eyalette bu ürün satın alınmamış olsun
-- UNION la birleştirip olmayanları EXCEPT ile çıkartabiliriz vs ama şimdi biz NOT EXIST ile yapacağız burada

-- Exist içine yukarıdaki sorguyu yapıştırıyoruz outer query de from dan sonra sale.customer C2 dedik
-- .. Çünkü bir şart eklemeliyiz(Altta açıklanıyor)
select	distinct [state]
from	sale.customer C2
where	not exists (
			select	distinct C.state
			from	product.product P,
					sale.order_item I,
					sale.orders O,
					sale.customer C
			where	P.product_name = 'Apple - Pre-Owned iPad 3 - 32GB - White' and
					P.product_id = I.product_id and
					I.order_id = O.order_id and
					O.customer_id = C.customer_id and
					C2.state = C.state
		)
;

-- Şartımız: C2.state = C.state : Yani, outer query de gelen statelerin inner query de olmama şartını inner query ye ekliyorum
-- EXIST ya da NOT EXIST i foreign keyler ya da primary keyler üzerinden yaparsak daha hızlı çalışır
-- .. Diğer türlü tüm tabloyu taraması gerekiyor
"""

#%% Dersin 2. bölümü
"""
--Soru: Burkes Outlet mağaza stoğunda bulunmayıp,
-- Davi techno mağazasında bulunan ürünlerin stok bilgilerini döndüren bir sorgu yazın

SELECT PC.product_id, PC.store_id, PC.quantity
FROM product.stock PC, sale.store SS
WHERE PC.store_id = SS.store_id AND SS.store_name = 'Davi techno Retail' AND
NOT EXISTS( SELECT DISTINCT A.product_id, A.store_id, A.quantity
FROM product.stock A, sale.store B
WHERE A.store_id = B.store_id AND B.store_name = 'Burkes Outlet' AND PC.product_id = A.product_id AND A.quantity>0)

--- Davi techno Retail da stoğu bulunnanları alacak
--- Burkes Outlet in stocklarında quantity>0 olanları not exists yapacak
--- quantityi belirtmeseydik;
--- çıktı hiçbir şey getirmedi. Buradan şu çıkıyor olabilir. Bu ürünlerin(Çıktıdaki 5 tane) Burkes outlet mağazaında satırları var
-- ancak bu ürünlerin stock miktarları 0.
-- sale.store tablosunu inner query ile kullanmadık ama yinede outer query de SS.store_name diyebiliriz

-- Bütün ürünlerimin stock bilgisi stock tablosunda var. Burkes in stoğunda 0 olarak gözüken ürünlerden bul diye de sonuca ulaşabiliriz
-- Exists ve quantity=0 diyerek
SELECT PC.product_id, PC.store_id, PC.quantity
FROM product.stock PC, sale.store SS
WHERE PC.store_id = SS.store_id AND SS.store_name = 'Davi techno Retail' AND
EXISTS( SELECT DISTINCT A.product_id, A.store_id, A.quantity
FROM product.stock A, sale.store B
WHERE A.store_id = B.store_id AND B.store_name = 'Burkes Outlet' AND PC.product_id = A.product_id AND A.quantity=0)

"""
"""
-- Soru: -- Brukes Outlet storedan alınıp The BFLO Store mağazasından hiç alınmayan ürün var mı?
-- Varsa bu ürünler nelerdir?
-- Ürünlerin satış bilgileri istenmiyor, sadece ürün listesi isteniyor.

SELECT P.product_name
FROM product.product P   
WHERE NOT EXISTS (
SELECt I.product_id
FROM sale.order_item I, sale.orders O, sale.store S
WHERE I.order_id = O.order_id AND S.store_id = O.store_id 
AND S.store_name = 'The BFLO Store' 
and P.product_id = I.product_id)

-- sorguya devam ediyoruz
-- P.product_name: product name geliyor ancak bu aşağıdaki kurala uymalı(subquery de)
-- NOT EXIST Dediğine göre birşeyleri eleyeceğiz. (The BFLO Store mağazasından hiç alınmayan)
-- Elemek istediğimiz yer: P.product_id = I.product_id  bu kod . Bütün product listemizde "The BFLO Store" dan sipariş edilmiş ürünleri eliyorum
-- Bir kriter daha vardı: Brukes Outlet storedan alınan o yüzden AND diyip EXISTS diyip devam ediyorum
-- Sonuç olarak 8 tane ürün geldi. 520 tane üründen 8 geldi
-- Tek sorguda product tablosunda istediğimiz 8 satırı seçmiş olduk

SELECT P.product_name, p.list_price, p.model_year
FROM product.product P
WHERE NOT EXISTS (
		SELECt	I.product_id
		FROM	sale.order_item I,
				sale.orders O,
				sale.store S
		WHERE	I.order_id = O.order_id AND S.store_id = O.store_id
				AND S.store_name = 'The BFLO Store'
				and P.product_id = I.product_id)
	AND
	EXISTS (
		SELECt	I.product_id
		FROM	sale.order_item I,
				sale.orders O,
				sale.store S
		WHERE	I.order_id = O.order_id AND S.store_id = O.store_id
				AND S.store_name = 'Burkes Outlet'
				and P.product_id = I.product_id)
;
    
--- Bunu yine except ile yapabilirdik

SELECT	distinct I.product_id
		FROM	sale.order_item I,
				sale.orders O,
				sale.store S
		WHERE	I.order_id = O.order_id AND S.store_id = O.store_id
				AND S.store_name = 'Burkes Outlet'
except
		SELECT	distinct I.product_id
		FROM	sale.order_item I,
				sale.orders O,
				sale.store S
		WHERE	I.order_id = O.order_id AND S.store_id = O.store_id
				AND S.store_name = 'The BFLO Store'
;

"""

##########################################
# CTE(Common Table Expressions)
# Bir VIEW gibi çalışırlar.
# Sorgu sürecinde o sırada meydana gelip daha sonra Sorgu sonunda kaybolan objelerdir.
# Sadece sorguya özgü VIEW diyebiliriz.
# ALL CTEs(ordinary or recursive) stat with a "WITH" clause ...
# Bir common table içinde birden fazla WITH clause kullanılabilir
# 2. çeşiti var 1.Ordinary 2. Recursive

############
# 1.Ordinary Common Table Expressions
"""
WITH query_name [(column_name1, ...)] AS
(SELECT ... ) -- CTE Definition

SQL_Statement; -- yukarda tanımlamış olduğumuz tabloyu kullanıyoruz bu statementta
"""
#############
# 2.Recursive Common Table Expressions
"""
WITH table_name (column_list) AS
.....
Hoca: devamı önemli değil çünkü ihtiyaç olunca gerekli kaynaklardan kopyala yapıştır yapacağız çalışırken

-- for döngüsü gibi kural tanımlayarak bir sorgu oluşturabiliyorsunuz
"""
######

#######################################
# 1.Ordinary Common Table Expressions
"""
# Soru: -- Jerald Berray isimli müşterinin son siparişinden önce sipariş vermiş 
--ve Austin şehrinde ikamet eden müşterileri listeleyin.

SELECT * FROM sale.customer a, sale.orders b
WHERE a.first_name = 'Jerald' and a.last_name ='Berray'
and a.customer_id = b.customer_id 

-- her yılda 1 er tane sipariş var. Buradan max(order_date i seçeceğiz)

SELECT  max(b.order_date) FROM sale.customer a, sale.orders b
WHERE a.first_name = 'Jerald' and a.last_name ='Berray'
and a.customer_id = b.customer_id 

--- bu elimizde dursun. Şimdi austin şehrinde ikamet edenlere bakalım
SElect * from sale.customer a 
where a.city = 'Austin'
--42 rows

----

SElect * from sale.customer a , sale.orders b
where a.city = 'Austin' and a.customer_id = b.customer_id
--35 row.. hepsinin sipariş bilgisi yokmuş

--- WITH i kullanalım

with tbl AS (
	select	max(b.order_date) JeraldLastOrderDate
	from	sale.customer a, sale.orders b
	where	a.first_name = 'Jerald' and a.last_name = 'Berray'
			and a.customer_id = b.customer_id
)
select	*
from	sale.customer a,
		Sale.orders b,
		tbl c
where	a.city = 'Austin' and a.customer_id = b.customer_id and
		b.order_date < c.JeraldLastOrderDate
;


--- b.order_date < c.JeraldLastOrderDate koşulu sona eklemiş olduk

"""

#%% Dersin 3. bölümü
# NOT : With clause sadece tek bir sorguda çalışıyor. 
# Fakat with bloğunda birden fazla sorgu tanımlayabilirsiniz
# Bununla ilgili bir örnek yapalım

"""
-- Herbir markanın satıldığı en son tarihi bir CTE sorgusunda,
-- Yine herbir markaya ait kaç farklı ürün bulunduğunu da ayrı bir CTE sorgusunda tanımlayınız.
-- Bu sorguları kullanarak  Logitech ve Sony markalarına ait son satış tarihini ve toplam ürün sayısını (product tablosundaki) aynı sql sorgusunda döndürünüz

with tbl as(
	select	br.brand_id, br.brand_name, max(so.order_date) LastOrderDate
	from	sale.orders so, sale.order_item soi, product.product pr, product.brand br
	where	so.order_id=soi.order_id and
			soi.product_id = pr.product_id and
			pr.brand_id = br.brand_id
	group by br.brand_id, br.brand_name
) ,  ---1. tablo sonucunda her bir product ın son sipariş tarihi . 23 brand_id li DENAQ 2020-04-23 te en son sipariş verilmiş
tbl2 as(
	select	pb.brand_id, pb.brand_name, count(*) count_product
	from	product.brand pb, product.product pp
	where	pb.brand_id=pp.brand_id
	group by pb.brand_id, pb.brand_name
)  ---2. tabloda Her bir markada kaç ürünün bulunduğu. 40 satır geldi
select	*
from	tbl a, tbl2 b
where	a.brand_id=b.brand_id and
		a.brand_name in ('Logitech', 'Sony')

--- Sony markasına ait herhangi bir ürün en son 2020-10-21 de sipariş verilmiş
--- ve sony markasına ait envanterimde 46 ürün varmış 
--- Logitect markasına ait herhangi bir ürün en son 2020-08-23 de sipariş verilmiş
--- ve sony markasına ait envanterimde 27 ürün varmış
"""

###################
# Recursive CTE Expressions
# İçerisinde UNION ALL yazıp CTE içerisinde belirtmiş olduğumuz tabloyu kullanacağız recursive şekilde
"""
-- 0'dan 9'a kadar herbir rakam bir satırda olacak şekide bir tablo oluşturun.
-- Normalde kalıbımız aşağıdaki gibi
WITH CTE AS ()
SELECT * from CTE;

-- Bu hata veriyor.Şimdi parantez içini dolduracağım
-- Tablo adım CTE olsun

WITH CTE AS (select 0 rakam UNION ALL select 1 rakam)  -- Bu şekilde 10 a kadar gidebiliriz
SELECT * from CTE;

--- Bunu dinamik yapalım adım adım ..DIKKAT Bu alttaki sonsuza kadar gider
WITH CTE AS (select 0 rakam UNION ALL select rakam+1)
SELECT * from CTE;

---WHERE bloğunda bunu sınırlayalım

WITH CTE AS (select 0 rakam UNION ALL select rakam+1 from cte where rakam<9)
SELECT * from CTE;
"""
# Raporlamada bu tip tablolar çok kullanıyorlar.
# PowerBI da bir database oluşturarak bunu kullanacaksınız
# DB ler genelde tarihler olur. Haftanın günü, tatil mi değil. O tarihin içinde bulunduğu ayın ilk günü, son günü vs
# .. gibi attribute lar olur. Bunlar çok büyük esneklik sağlar. Sizde CTE ile başlayıp böyle bir attribute(ya da tablo) oluşturabilirsiniz

"""
--Soru: 2020 ocak ayının herbir tarihi bir satır olacak şekilde 31 satırlı bir tablo oluşturunuz.
with cast('2020-01-01' as date) tarih  --- veriyi date olarak cast ettik

with ocak as (
	select	cast('2020-01-01' as date) tarih  --- veriyi date olarak cast ettik
	union all
	select	cast(DATEADD(DAY, 1, tarih) as date) tarih   -- üstteki "tarih" ile tanımlanana 1 ekle DATEADD(DAY, 1, tarih) as date datetime olarak geldiği için bunuda cast ettik
	from ocak
	where tarih < '2020-01-31'
)
select * from ocak;
with cte AS (
	select cast('2020-01-01' as date) AS gun
	union all
	select DATEADD(DAY,1,gun)
	from cte
	where gun < EOMONTH('2020-01-01')  --EOMONTH: ayın son gününü alır
) --- buradan sonra biz tarih tablosu oluşturalım
select gun tarih, day(gun) gun, month(gun) ay, year(gun) yil,
	EOMONTH(gun) ayinsongunu
from cte;

-- Siz bunun yanına tarih tablosu oluşturacaksanız ekleme yapabilirsiniz
-- Bu şekilde bir çok attribute oluşturursanız bu size çok büyük zenginlik kazandıracaktır.
-- her bir tablodaki tarih ile bu tabloyu joinlersiniz. Yani bu tarihleri diğer tablolarda kullanabilirsiniz.
-- Bunun çıkış noktası common table expressions
"""
###############
"""
--- Soru: Write a query that returns all staff with their manager_ids(use recursive CTE)
-- Her bir çalışanın patronuyla CTE sini alacağız burada

Select staff_id, first_name, manager_id from sale.staff where staff_id =1
 --- Şimdi de manager ı james olan kişileri getirelim
Select * from sale.staff a where a.manager_id = 1

-- Şimdi with ekleyelim ve where a.manager_id = 1 i manuel olarak almayacağım. Bir önce tanımlamış olduğum kişinin id sine(staff_id) sine eşitleyeceğiz

with cte as (
	select	staff_id, first_name, manager_id
	from	sale.staff
	where	staff_id = 1
	union all
	select	a.staff_id, a.first_name, a.manager_id
	from	sale.staff a, cte b
	where	a.manager_id = b.staff_id
)
select *
from	cte
;

--- a.manager_id = b.staff_id si 1 olanları çağır sonra   a.manager_id ye dönecek sonra sale.staff a tekrar gidecek tekrar
--- a.manager_id = b.staff_id  ye bakacak vs vs böyle devam edip En sonra manager_id si olmayana dönecek ve break olacak sorgumuz
--- Bu tip bir sorgu raporlama yaparken işe yarar yoksa şu şekilde de yapabilirdik.


select staff_id, first_name, manager_id
from sale.staff
order by manager_id
"""
#########
"""
--- Soru: --2018 yılında tüm mağazaların ortalama cirosunun altında ciroya sahip mağazaları listeleyin.
--List the stores their earnings are under the average income in 2018.
--- with clause un altında 2 tane tablo tanımlayacağız

WITH T1 AS (
SELECT	c.store_name, SUM(list_price*quantity*(1-discount)) Store_earn
FROM	sale.orders A, SALE.order_item B, sale.store C
WHERE	A.order_id = b.order_id
AND		A.store_id = C.store_id
AND		YEAR(A.order_date) = 2018
GROUP BY C.store_name
),
T2 AS (
SELECT	AVG(Store_earn) Avg_earn
FROM	T1
)
SELECT *
FROM T1, T2
WHERE T2.Avg_earn > T1.Store_earn
;

---1. tabloda Her bir store name her bir mağazanın yapmış olduğu satış tutarı. Filtre olarak da yıla 2018 dedik
---2.tabloda T1 deki değerlere göre ortalama aldık
--- Tabloları birbiri içerisinde referans gösterebiliyoruz
--- Final de T1,T2 tablosuna git T2 deki ortalama cironun T1 deki store cirolarından büyük olan mağazaları getir

"""










