select
	cast(gal8.dbo.ToInt64(mc.f$nrec) as varchar) as id,
	mc.f$name as name,
	mc.f$barkod as barcode
from gal8.dbo.t$katmc as mc with (nolock)
where mc.f$nrec in (select nrec from pradata_sku with (nolock))
