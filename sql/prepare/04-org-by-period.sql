-- Покупки товаров за период из документов:
--  * Накладная на отпуск МЦ (201)
--  * Рекламационная накладная от покупателя на возврат МЦ (106)
set nocount on;

declare @d_start date = :date_start;
declare @d_end date = :date_end;

if object_id('pradata_org_by_period', 'U') is not null
	drop table pradata_org_by_period;

select f$corg as nrec
into pradata_org_by_period
from (
    select f$nrec, f$corg, f$dsopr, f$vidsopr from gal_rs.dbo.t$katsopr with(nolock, index=3) union all
    select f$nrec, f$corg, f$dsopr, f$vidsopr from gal_pp.dbo.t$katsopr with(nolock, index=3) union all
    select f$nrec, f$corg, f$dsopr, f$vidsopr from gal_erder.dbo.t$katsopr with(nolock, index=3) union all
    select f$nrec, f$corg, f$dsopr, f$vidsopr from gal_kpss.dbo.t$katsopr with(nolock, index=3)
) as k
join (
    select f$csopr, f$cmcusl from gal_rs.dbo.t$spsopr with (nolock) union all
    select f$csopr, f$cmcusl from gal_pp.dbo.t$spsopr with (nolock) union all
    select f$csopr, f$cmcusl from gal_erder.dbo.t$spsopr with (nolock) union all
    select f$csopr, f$cmcusl from gal_kpss.dbo.t$spsopr with (nolock)
) as s on k.f$nrec = s.f$csopr
where k.f$vidsopr in (106, 201)
	and s.f$cmcusl in (select nrec from pradata_sku with (nolock))
    and k.f$corg not in (select f$nrec from pradata_our_orgs with (nolock))
and k.f$dsopr between gal8.dbo.toAtlDate(@d_start) and gal8.dbo.toAtlDate(@d_end)