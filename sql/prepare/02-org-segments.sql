set nocount on;

-- Канал сбыта
declare @classcode as int = 33
-- Таблица: каталог организаций
declare @wtable as int = 1448

if object_id('pradata_org_segments', 'U') is not null
	drop table pradata_org_segments;

select
	val.f$crec as nrec,
	seg.f$name as kanal
into pradata_org_segments
from gal8.dbo.t$exclassval as val with (nolock)
left join gal8.dbo.t$exclassseg as seg with (nolock) on seg.f$nrec = val.f$cclassseg
where f$wtable = @wtable and val.f$classcode = @classcode