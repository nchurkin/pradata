set nocount on;

-- Таблица: каталог МЦ
declare @wtable as int = 1411
-- код атрибута поставщик в attrval
declare @post as binary(8) = 0x8007000000000004

if object_id('pradata_sku', 'U') is not null
	drop table pradata_sku;

select f$crec as nrec
into pradata_sku
from gal8.dbo.t$attrval with (nolock)
where f$wtable = @wtable
	and f$vstring in ('Forgenika', 'OSQ')
	and f$cattrnam = @post
