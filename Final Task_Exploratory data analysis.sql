\\task 1\\

select 
	"Marital Status" as marital_status, 
	round(avg(age),2) as avg_age
from 
	customer
where
	"Marital Status"  != ''
group by 
	marital_status
order by
	avg_age asc 	

	
	\umur\
--select     
--	CASE
--        WHEN age < 25 THEN '... - 25'
--        WHEN age BETWEEN 25 and 30 THEN '25 - 30'
--        WHEN age BETWEEN 30 and 35 THEN '30 - 35'
--        WHEN age >= 35 THEN '35 - ...'
--        WHEN age IS NULL THEN '(NULL)'
--    END as range_umur,
--    COUNT(*) AS jumlah
--from customer 
--GROUP BY range_umur
--ORDER BY range_umur
	
\\task 2\\

select 
	gender,
	round(avg(age),2) as avg_age
from 
	customer 
group by
	gender 
order by
	avg_age asc

	
\\task 3\\

select
	st.storename as store_name,
	sum(tr.qty) as quantity
from
	transaction as tr
join	
	store as st
	on
	tr.storeid = st.storeid
group by 
	store_name
order by 
	quantity desc
	
 //task 4//
 
select
	prd."Product Name" as product_name,
	sum(trn.totalamount) as total_amount
from
	product prd
join
	"transaction" trn
	on
	prd.productid = trn.productid 
group by 
	product_name
order by 
	total_amount desc
	
	