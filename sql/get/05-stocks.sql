/*
Остатки товаров на дату (на конец дня)
*/

declare @date date = :date

select
	@date as [date],
	cast(gal8.dbo.ToInt64(sku.nrec) as varchar) as sku_id,
	isnull(t.qty, 0) as qty
from pradata_sku as sku
left join (

	select
		saldo.f$cmc as cmc,
		cast(sum(saldo.f$kol) as numeric(17, 2)) as qty
	from gal8.dbo.t$saldomc as saldo
	right join (
		select
			f$cmc, f$cparty, f$cpodr, f$cmol, max(f$dsaldo) as f$dsaldo
		from gal8.dbo.t$saldomc with (nolock)
		where
			f$cpodr <> 0x8000000000000000 and
			f$cmol = 0x8000000000000000 and
			f$sp = 0 and
			f$dsaldo <= gal8.dbo.ToAtlDate(dateadd(day, 1, @date))
		group by f$cmc, f$cparty, f$cpodr, f$cmol
		) as tmpsaldo on
			tmpsaldo.f$cmc = saldo.f$cmc and
			tmpsaldo.f$cparty = saldo.f$cparty and
			tmpsaldo.f$cpodr = saldo.f$cpodr and
			tmpsaldo.f$cmol = saldo.f$cmol and
			tmpsaldo.f$dsaldo = saldo.f$dsaldo and
			saldo.f$kol <> 0
	where saldo.f$cmc in (select nrec from pradata_sku)
	and saldo.f$cpodr in (
			select f$nrec from gal8.dbo.t$katpodr where f$cpodr = 0x8007000000000001 union all	-- Склад 1
			select f$nrec from gal8.dbo.t$katpodr where f$cpodr = 0x8008000000000001 union all	-- Склад 2
			select f$nrec from gal8.dbo.t$katpodr where f$cpodr = 0x800100000000000C union all	-- Склад 3
			select f$nrec from gal8.dbo.t$katpodr where f$cpodr = 0x8025000000000001			-- Склад 4
		)
	group by saldo.f$cmc

) as t on sku.nrec = t.cmc