#%% SQL-14. ders_16.06.2022(son session)

#%%
# Table of Contents: # Stored procedures: # User Defined/Valued Functions

# Stored procedures : DB tarafında insert,update, alter vs gibi işlemlerle ilgili kullanıyoruz
    # .. Örneğin: denormalize verisetini normalize hale getirmeniz gerekiyor. Bunu sürekli
    # .. yapmanız gerekiyor. Siz bir stored procedures oluşturursunuz. Bunu kaydediyorsunuz.
    # .. Bu günde 1 çalışsın ya da şu tablo üzerinde çalışsın diyebiliyoruz
    # .. Arka plan işlerinin yapıldığı yer olarak düşünebiliriz
    # User Defined/Valued Function: Fonksiyon adı üzerinde , DDL de fonksiyonlar kullanılmaz, 
    # Yararları: Performance, Maintainability, Productivity and Easy to Use, Security

##########################
# 1.STORED PROCEDURES
"""
select 'Hello World!'
-- Bu sorguyu bir procedure ile çalıştıralım

create procedure sp_sampleproc1 as
select 'Hello World!';
-- sonra bu kaydettiğim procedure u çalıştırıyorum bunu
EXEC sp_sampleproc1
-- asıl kod(2. yol): EXECUTE sp_sampleproc1 --
"""

#%% Dersin 2. bölümü
# BEGIN & END
# Bir sorgu kümesinin başladığını ve bittiğini ifade eder
"""
create procedure sp_sampleproc2 as
BEGIN
select 'Hello World!';
END
--
EXEC sp_sampleproc2
"""

# Procedure de bir silmek,  değişiklik istersek drop edip sonra tekrar oluşturabiliriz
"""
drop procedure sp_sampleproc2
-- tekrar create edelim
create procedure sp_sampleproc2 as
BEGIN
select 'Hello World!';
END
--
EXECUTE sp_sampleproc2;

-- Değiştirmek
alter procedure sp_sampleproc1
AS
begin
select 'Hello World 3 !'
end
;
--
EXECUTE sp_sampleproc1;
"""

# Create ettiğimiz procedure leri MS-SQL de nasıl göreceğiz
# Sample Retail -- Programmability--Stored Procedures --> (Burada görebiliriz)
# NOT: System Store Procedures: Bunlar DB nin düzgün işlemesini sağlayan sistem procedure leri

# Tablo create edip, veri insert edeceğiz Sample retail e
"""
CREATE TABLE ORDER_TBL 
(
ORDER_ID TINYINT NOT NULL,
CUSTOMER_ID TINYINT NOT NULL,
CUSTOMER_NAME VARCHAR(50),
ORDER_DATE DATE,
EST_DELIVERY_DATE DATE--estimated delivery date
);
----------------------------------------
INSERT INTO ORDER_TBL VALUES (1, 1, 'Adam', GETDATE()-10, GETDATE()-5 ),
						(2, 2, 'Smith',GETDATE()-8, GETDATE()-4 ),
						(3, 3, 'John',GETDATE()-5, GETDATE()-2 ),
						(4, 4, 'Jack',GETDATE()-3, GETDATE()+1 ),
						(5, 5, 'Owen',GETDATE()-2, GETDATE()+3 ),
						(6, 6, 'Mike',GETDATE(), GETDATE()+5 ),
						(7, 6, 'Rafael',GETDATE(), GETDATE()+5 ),
						(8, 7, 'Johnson',GETDATE(), GETDATE()+5 )
---------------------------------------
select * from ORDER_TBL
"""
# Başka bir tablo daha create edeceğiz
"""
CREATE TABLE ORDER_DELIVERY
(
ORDER_ID TINYINT NOT NULL,
DELIVERY_DATE DATE -- tamamlanan delivery date
);
----------------------------------------
SET NOCOUNT ON -- çıktı da 8 rows affected diye uyarı gelmiyor
INSERT ORDER_DELIVERY VALUES (1, GETDATE()-6 ),
				(2, GETDATE()-2 ),
				(3, GETDATE()-2 ),
				(4, GETDATE() ),
				(5, GETDATE()+2 ),
				(6, GETDATE()+3 ),
				(7, GETDATE()+5 ),
				(8, GETDATE()+5 )
----------------------------------------    
select * from ORDER_DELIVERY      
"""
# 2 tablomuz var. Order tablosu sürekli değişecek. Öyle bir procedure yazayım ki order_tbl deki
# .. satır sayısını döndürsün
"""
CREATE procedure sp_sum_order
as
BEGIN
select count(*) as TOTAL_ORDER
from ORDER_TBL
END
--- Procedure ü çağıralım
EXECUTE sp_sum_order
"""

# Herhangi bir tarih girip. O tarih sayısındaki sipariş sayısını döndürsün
# Bunun için input tanımlamamız gerekiyor
"""
CREATE PROCEDURE sp_wantedday_order (@DAY DATE) AS
BEGIN
select count(*) as TOTAL_ORDER
from ORDER_TBL
where ORDER_DATE = @DAY
END
-- Eğer input tanımlayacaksam procedure un isminden sonra parametre adı(DAY) sonra veritipini(DATE) yazıyorum
-- Procedure ü nasıl çağıracağız
EXECUTE sp_wantedday_order '2022-06-22'
-- sp_wantedday_order procedure e gidecek  '2022-06-22' a bakacak day parametresi ile
-- Çıktı da 3 geldi
"""

# DECLARE: Bir parametreye değer atayıp bu parametreyi sorgularımda kullanabilirim.
"""
DECLARE
@p1 INT,
@p2 INT,
@SUM INT
SET @p1 = 5  -- parametrenin birine değer atadık
SELECT @p1 -- Output: 5
--
DECLARE
	@p1 INT,
	@p2 INT,
	@SUM INT
SET @p1 = 5
SELECT *
from ORDER_TBL
where ORDER_ID = @p1

-- p1: Parametre 1
-- SET ile parametreye veri atadık
------------------------------------------
-- order_id si 5 olan müşterinin customer_name i getireceğiz
DECLARE
	@order_id INT,
	@customer_name nvarchar(100)
SET @order_id = 5
SELECT @customer_name = customer_name
from ORDER_TBL
where ORDER_ID = @order_id
select @customer_name
-- select @customer_name : customer_name e gelen sonuç
-- where order_id > @order_id : ... şeklinde bir yapı kullanabiliriz
-- Burası OOP olarak geçiyor
------------------------------------------
declare
	@day date
set @day = getdate()-2     -- bugünden itibaren 2 gün öncesinde kayıt varsa getiriyor
EXECUTE sp_wantedday_order @day
;
"""

#%% Dersin 3. bölümü
####################
# 2.FUNCTIONS
# Table-Valued Function -- > Tablo döndürür
# Scalar-Valued Functions -- > Değer döndürür


"""
-- Scalar-Valued Functions örnek
-- Input alarak almış olduğu metni büyük harfe çeviren fonksisyon
CREATE FUNCTION fnc_uppertext
(
	@inputtext varchar (MAX)
)
RETURNS VARCHAR (MAX)
AS
BEGIN
	RETURN UPPER(@inputtext)
END

-- Fonksiyonumuzu tanımladık
-- NOT:Declare ile parametreler atıyabilirdik
-- Bu fonksiyonu nasıl kullanacağız bakalım
SELECT dbo.fnc_uppertext('Hello world')
-- fonksiyonu create ederken şema adı vermezsek "dbo" altında ister bunu çağırırken o yüzden "dbo" yazmamız gerekli

-------------------------------------------------
-- Table-Valued Funtions örnek
-- Müşteri adını parametre olarak alıp o müşterinin alışverişlerini döndüren bir fonksiyon yazınız.
-- Önce bunun sorgusunu yazalım sonra fonksiyon yazalım
Select * from ORDER_TBL where customer_name = 'Smith'
--
CREATE FUNCTION fnc_getordersbycustomer1(@CUSTOMER_NAME NVARCHAR(100))
RETURNS TABLE AS
RETURN
Select * from ORDER_TBL where customer_name = @CUSTOMER_NAME

-- @CUSTOMER_NAME: input parametresi
-- Bu fonksiyon tablo döndürecek. O yüzden bunu tabloyu yazabildiğimiz yerde yazacağız(Mesela "from" dan sonra)
--
select * from dbo.fnc_getordersbycustomer1('Owen')
-- Owen ın siparişleri geldi
"""

#############
# IF / ELSE
# IF den sonra koşul, sonra koşu varsa "else if", "else if" vs yapacağız

"""
-- Bir fonksiyon yazınız. Bu fonksiyon aldığı rakamsal değeri çift ise çift, tek ise tek döndürsün
-- Eğer 0 ise sıfır döndürsün. 3 tane koşul
-- Önce bir sayının tek veya çift olduğunu anlamak için "mod" kullanacağız
DECLARE
    @input int,
    @modulus int

SET @input = 10
SELECT @input % 2
--------------------------
DECLARE
    @input int,
    @modulus int

SET @input = 10
SELECT @modulus = @input % 2
-- Çıktı yok çıktı için
DECLARE
    @input int,
    @modulus int

SET @input = 10
SELECT @modulus = @input % 2
PRINT @modulus
------------------
-- Şimdi bu alttaki mantığı kullanacağız
IF ...
	BEGIN
	...
	END
ELSE IF ...
	BEGIN
	...
	END
ELSE ...
--------------------input u tek olacak şekilde yapalım
DECLARE
	@input int,
	@modulus int
SET @input = 5
SELECT @modulus = @input % 2
IF @input = 0
	BEGIN
	 print 'Sıfır'
	END
ELSE IF @modulus = 0
	BEGIN
	 print 'Çift'
	END
ELSE print 'Tek'
-------------------- input u çift yapalım
DECLARE
	@input int,
	@modulus int
SET @input = 10
SELECT @modulus = @input % 2
IF @input = 0
	BEGIN
	 print 'Sıfır'
	END
ELSE IF @modulus = 0
	BEGIN
	 print 'Çift'
	END
ELSE print 'Tek'
-- Bunun üzerine fonksiyonu create edeceğiz
------------------------------------------
create FUNCTION dbo.fnc_tekcift
(
	@input int
)
RETURNS nvarchar(max)
AS
BEGIN
	DECLARE
		-- @input int,
		@modulus int,
		@return nvarchar(max)
	-- SET @input = 100    -- NOT:Bunu kaldırırsak her zaman çift değerini döndürecekti. Ama sonuç bizim girdiğimiz parametreye bağlı oldu burayı kaldırdığımız için
	SELECT @modulus = @input % 2
	IF @input = 0
		BEGIN
		 set @return = 'Sıfır'
		END
	ELSE IF @modulus = 0
		BEGIN
		 set @return = 'Çift'
		END
	ELSE set @return = 'Tek'
	return @return
	
END
;

-- if bloğundaki her bir değerde @return ün eşitindekileri atayacak('Sıfır','Çift','Tek')
-- if yapısında @return parametreme değer atamış oldum o yüzden en sonra return olarak @return ü döndürdük
-- Fonsiyon tanımlarken yazdırma değil de return yapacağımız için printler yerine return yazdık
-- input parametresini fonksiyon içinde tanımladığımız için DECLARE içinde tekrar tanımlamadık hata almamak için
-- Bunu scalar value ların olduğu yerde kullanabiliriz. Mesela select bloğunda, where bloğunda vs
select dbo.fnc_tekcift(100) A, dbo.fnc_tekcift(9) B,dbo.fnc_tekcift(0) C
"""

###########
# WHILE
# Belli bir sayıda bir şey dönmesini istiyorsak kullanıyoruz
"""
-- 1 den 50 ye kadar olan sayıları yazdıralım
select 1
-----------
PRINT 1
----------
-- Biz parametreleri belirleyelim
-- 1 den başlayacağını belirleyeceğimiz parametremizi oluşturalım
DECLARE
    @counter int

set @counter= 1
PRINT @counter
PRINT @counter + 1
PRINT @counter + 2
PRINT @counter + 3
-- Şimdi burada bir yerde durmasını istediğimiz için total parametresini de ekleyelim
-- counter ımız artacak sürekli ve total dan küçük olduğu sürece yazdıracak
DECLARE
	@counter int,
	@total int
set @counter = 1
set @total = 50
while @counter < @total
	begin
		PRINT @counter
		set @counter = @counter + 1
	end
;

-- Hoca: begin ve end i belirtmemiz gerekiyor
"""

"""
--Siparişleri, tahmini teslim tarihleri ve gerçekleşen teslim tarihlerini kıyaslayarak
--'Late','Early' veya 'On Time' olarak sınıflandırmak istiyorum.
--Eğer siparişin ORDER_TBL tablosundaki EST_DELIVERY_DATE' i (tahmini teslim tarihi) 
--ORDER_DELIVERY tablosundaki DELIVERY_DATE' ten (gerçekleşen teslimat tarihi) küçükse
--Bu siparişi 'LATE' olarak etiketlemek,
--Eğer EST_DELIVERY_DATE>DELIVERY_DATE ise Bu siparişi 'EARLY' olarak etiketlemek,
--Eğer iki tarih birbirine eşitse de bu siparişi 'ON TIME' olarak etiketlemek istiyorum.
--Daha sonradan siparişleri, sahip oldukları etiketlere göre farklı işlemlere tabi tutmak istiyorum.
--istenilen bir order' ın status' unu tanımlamak için bir scalar valued function oluşturacağız.
--çünkü girdimiz order_id, çıktımız ise bir string değer olan statu olmasını bekliyoruz.

-- ilk önce sorgumuzu yazalım adım adım
select * from ORDER_TBL A, ORDER_DELIVERY B
WHERE A.ORDER_ID = B.ORDER_ID
------------------------------------
create FUNCTION dbo.fnc_orderstatus
(
	@input int
)
RETURNS nvarchar(max)
AS
BEGIN
	declare
		@result nvarchar(100)
	-- set @input = 1
	select	@result =
				case
					when B.DELIVERY_DATE < A.EST_DELIVERY_DATE
						then 'EARLY'
					when B.DELIVERY_DATE > A.EST_DELIVERY_DATE
						then 'LATE'
					when B.DELIVERY_DATE = A.EST_DELIVERY_DATE
						then 'ON TIME'
				else NULL end
	from	ORDER_TBL A, ORDER_DELIVERY B
	where	A.ORDER_ID = B.ORDER_ID AND
			A.ORDER_ID = @input
	;
	return @result
end
;
-- Case aslında 1 değer döndürüyor. Bu döndüren değeri bir parametreye atayacağız yani,
-- case içindeki ifadeleride bir parametreye atayalım yoksa kodda "where" de order_id ye değer vermem gerekiyor
-- .. onun yerin @input değeri gireceğiz orada
-- fonksiyonu çağıralım
select	dbo.fnc_orderstatus(3);
-- şu şekilde de çalıştırabilirdik fonksiyonu;
-- fonksiyonun döndürdüğü bir scalar value olduğu fonksiyon içine parametre olarak ORDER_ID yazarsak select bloğunda hepsi için sonucu alabiliriz
select	*, dbo.fnc_orderstatus(ORDER_ID) OrderStatus
from	ORDER_TBL ;
"""













