SELECT
	ajb.[ats_id]
	,ajb.[ats_name]
	,ajb.[job_board_id]
	,ajb.[job_board_name]
	--last_scrape_log.*
FROM [data_site].[dbo].[ats_job_board] as ajb
left join
(
	select *
	from
	(
        SELECT
            [scrape_id]
            ,[year_month]
            ,[ats_id]
            ,[job_board_id]
            ,[succeeded_or_failed]
            ,[load_date]
            ,row_number() over (partition by year_month, ats_id, job_board_id order by load_date desc) as ranking
          FROM [data_site].[dbo].[scrape_log]
     ) as sub
	 where ranking = 1
) as last_scrape_log
	on ajb.ats_id = last_scrape_log.ats_id
	and ajb.job_board_id = last_scrape_log.job_board_id
	and '${year_month}' = last_scrape_log.year_month
where last_scrape_log.ats_id is null or last_scrape_log.[succeeded_or_failed] = 0


