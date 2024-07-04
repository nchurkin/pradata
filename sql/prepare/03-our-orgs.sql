set nocount on;

if object_id('pradata_our_orgs', 'U') is not null
	drop table pradata_our_orgs;

select
	f$nrec,
	f$name
into pradata_our_orgs
from gal8.dbo.t$katorg as org with (nolock)
where left(org.f$name, 1) = ' '
