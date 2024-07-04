declare @distr_code as int = 17

SELECT
    client_code,
    client_name,
	'Адрес клиента ' + cast(gal8.dbo.ToInt64(parent_nrec) as varchar) client_addr,
    client_name + '/ТТ ' + cast(gal8.dbo.ToInt64(child_nrec) as varchar) tt_name,
    'Адрес ТТ ' + cast(gal8.dbo.ToInt64(child_nrec) as varchar) tt_addr,
    inn,
    segment
FROM pradata_org_w_tt_by_period with (nolock)