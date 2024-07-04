set nocount on;
declare @date_start date = :date_start;
declare @date_end date = :date_end;

if object_id('pradata_docs_by_period', 'U') is not null
	drop table pradata_docs_by_period;

select
    k.f$nrec as nrec,
    k.f$vidsopr as vidsopr
into pradata_docs_by_period
from (
    select * from gal_rs.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_pp.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_erder.dbo.t$katsopr with(nolock, index=3) union all
    select * from gal_kpss.dbo.t$katsopr with(nolock, index=3)
) as k
join (
    select * from gal_rs.dbo.t$spsopr with(nolock) union all
    select * from gal_pp.dbo.t$spsopr with(nolock) union all
    select * from gal_erder.dbo.t$spsopr with(nolock) union all
    select * from gal_kpss.dbo.t$spsopr with(nolock)
) as s on s.f$csopr = k.f$nrec
where k.f$vidsopr in (106, 201)
    and s.f$cmcusl in (select nrec from pradata_sku with (nolock))
    and k.f$dsopr between gal8.dbo.toAtlDate(@date_start) and gal8.dbo.toAtlDate(@date_end)