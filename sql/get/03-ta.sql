select
  isnull(co.f$code, 'нет') as ta_code,
  isnull(co.f$name, 'нет') as ta_name
from gal_rs.dbo.t$katsopr as ks with (nolock)
left join gal8.dbo.t$fpco as co with (nolock) on co.f$nrec = f$cotvpodr
where ks.f$nrec in (
    select nrec from pradata_docs_by_period  with (nolock) where vidsopr = 201
)
group by co.f$code, co.f$name