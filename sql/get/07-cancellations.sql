declare @date date = :date

select
	gal8.dbo.ToInt64(sku.nrec) as sku_id,
	@date as [date],
	isnull(t.qty, 0) as qty,
	isnull(t.doc_num, '') as doc_num
from pradata_sku as sku
left join (
	select
		spo.f$cmc as cmc,
		sum(cast(spo.f$kol as numeric(17, 2))) * case when o.f$vidorder = 1 then -1 else 1 end as qty,
		ks.f$nsopr as doc_num
	from gal8.dbo.t$sklorder as o with(nolock)
	join gal8.dbo.t$sporder as spo with(nolock) on o.f$nrec = spo.f$csklorder
	join (
		select * from gal_rs.dbo.t$katsopr with(nolock) union all
		select * from gal_pp.dbo.t$katsopr with(nolock) union all
		select * from gal_erder.dbo.t$katsopr with(nolock) union all
		select * from gal_kpss.dbo.t$katsopr with(nolock)
	) as ks on ks.f$nrec = o.f$csopr
	where gal8.dbo.IntToDate(o.f$dord) = @date
	    and spo.f$cparty <> 0
		and spo.f$cmc in (select nrec from pradata_sku)
		and ks.f$vidsopr not in (101, 106, 201, 206)
	group by o.f$vidorder, ks.f$vidsopr, ks.f$nsopr, ks.f$dsopr, spo.f$cmc
) as t on t.cmc = sku.nrec