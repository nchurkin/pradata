declare @date date = :date

select
	gal8.dbo.ToInt64(sku.nrec) as sku_id,
	@date as [date],
	isnull(t.qty, 0) as qty,
	isnull(t.doc_num, '') as doc_num
from pradata_sku as sku
left join (

	select
		gal8.dbo.IntToDate(ks.f$dopr) as [date],
		sp.f$cmcusl as cmc,
		case
			when ks.f$vidsopr = 101 then cast(sum(sp.f$kolfact) as numeric(17, 2))
			when ks.f$vidsopr = 206 then cast(sum(sp.f$kolfact) as numeric(17, 2)) * -1
		end as qty,
		ks.f$nsopr as doc_num
	from (
		select * from gal_rs.dbo.t$katsopr union all
		select * from gal_pp.dbo.t$katsopr union all
		select * from gal_erder.dbo.t$katsopr union all
		select * from gal_kpss.dbo.t$katsopr
	) as ks
	join (
		select * from gal_rs.dbo.t$spsopr union all
		select * from gal_pp.dbo.t$spsopr union all
		select * from gal_erder.dbo.t$spsopr union all
		select * from gal_kpss.dbo.t$spsopr
	) as sp on sp.f$csopr = ks.f$nrec
	where
		sp.f$cmcusl in (select nrec from pradata_sku) and
		ks.f$vidsopr in (101, 206) and
		gal8.dbo.IntToDate(ks.f$dopr) = @date
		and ks.f$corg not in (select f$nrec from pradata_our_orgs)
	group by ks.f$dopr, ks.f$nsopr, ks.f$vidsopr, sp.f$cmcusl

) as t on t.cmc = sku.nrec
