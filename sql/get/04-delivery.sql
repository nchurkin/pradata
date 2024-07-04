select
	tt.client_code as client_code,
	gal8.dbo.IntToDate(ks.f$dopr) [date],
    cast(gal8.dbo.ToInt64(mc.f$nrec) as varchar) as sku_id,
	isnull(
        case
            when ks.f$vidsopr = 201 then cast(sum(sp.f$kolfact) as numeric(17, 2))
            when ks.f$vidsopr = 106 then cast(sum(sp.f$kolfact) as numeric(17, 2)) * -1
        end, 0) as qty,
	cast(
		round(
			case when ks.f$vidsopr = 106
				then (case when ks.f$vhodnal in (0, 2) then sp.f$price else sp.f$price - sp.f$sumnds / sp.f$kolfact end * sum(sp.f$kolfact)) * -1
				else (case when ks.f$vhodnal in (0, 2) then sp.f$price else sp.f$price - sp.f$sumnds / sp.f$kolfact end * sum(sp.f$kolfact))
			end,
			2
		) as numeric(17, 2)) as total,
	cast(
		round(
			case when ks.f$vidsopr = 106
				then (case when ks.f$vhodnal = 1 then sp.f$price else sp.f$price + sp.f$sumnds / sp.f$kolfact end * sum(sp.f$kolfact)) * -1
				else (case when ks.f$vhodnal = 1 then sp.f$price else sp.f$price + sp.f$sumnds / sp.f$kolfact end * sum(sp.f$kolfact))
			end,
		2) as numeric(17, 2)) as total_gross,
	isnull(co.f$code, 'нет') as ta_code,
	ks.f$nsopr as doc_num
from (
    select * from gal_rs.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_pp.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_erder.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_kpss.dbo.t$katsopr with(nolock, index=3)
) as ks
join (
    select * from gal_rs.dbo.t$spsopr with(nolock) union all
    select * from gal_pp.dbo.t$spsopr with(nolock) union all
    select * from gal_erder.dbo.t$spsopr with(nolock) union all
    select * from gal_kpss.dbo.t$spsopr with(nolock)
) as sp on sp.f$csopr = ks.f$nrec
join gal8.dbo.t$katmc mc with(nolock)  on mc.f$nrec=sp.f$cmcusl
join pradata_org_w_tt_by_period tt with(nolock) on tt.child_nrec = ks.f$corg
left join gal8.dbo.t$fpco co with(nolock)  on co.f$nrec = f$cotvpodr
where ks.f$nrec in (select nrec from pradata_docs_by_period with(nolock))
    and mc.f$nrec in (select nrec from pradata_sku with(nolock))
	and ks.f$corg not in (select f$nrec from pradata_our_orgs with(nolock))
    and ks.f$dopr <> gal8.dbo.toAtlDate(cast(year(getdate()) as nvarchar) + '-12-31')
group by tt.client_code, ks.f$dopr, mc.f$nrec, ks.f$vidsopr, ks.f$vhodnal, sp.f$price, sp.f$sumnds, sp.f$kolfact, co.f$code, ks.f$nsopr