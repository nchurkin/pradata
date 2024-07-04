set nocount on;

if object_id('pradata_org_w_tt_by_period', 'U') is not null
	drop table pradata_org_w_tt_by_period;

select
	parent_nrec,
	child_nrec,
	cast(gal8.dbo.toInt64(companies.parent_nrec) as varchar) + '#' + cast(gal8.dbo.toInt64(companies.child_nrec) as varchar) as client_code,
	parent_name as client_name,
	parent_addr as client_addr,
	child_name as tt_name,
	child_addr as tt_addr,
	parent_inn as inn,
	isnull(seg.kanal, N'не установлен') as segment
into pradata_org_w_tt_by_period
from (
	select
		f$nrec as parent_nrec,
		f$nrec as child_nrec,
		f$name as parent_name,
		f$addr as parent_addr,
		f$name as child_name,
		f$addr as child_addr,
		f$unn as parent_inn
	from gal8.dbo.t$katorg as org with(nolock)

	union

	select
		parent.f$nrec as parent_nrec,
		child.f$nrec as child_nrec,
		parent.f$name as parent_name,
		parent.f$addr as parent_addr,
		child.f$name as child_name,
		child.f$addr as child_addr,
		parent.f$unn as parent_inn
	from gal8.dbo.t$katorg as parent with(nolock)
	join (
		select * from gal8.dbo.t$katorg with(nolock) where f$shortname like '__%__%' escape '_' and f$shortname not like '__000001__%' escape '_'
	) as child on substring(child.f$shortname, 2, charindex('_', child.f$shortname, 2) - 2) = parent.f$code
) as companies
left join pradata_org_segments as seg with(nolock) on seg.nrec = companies.parent_nrec
where companies.parent_nrec in (select nrec from pradata_org_by_period with(nolock))
