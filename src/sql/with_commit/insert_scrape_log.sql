INSERT INTO dbo.scrape_log ([year_month], [ats_id], [job_board_id], [succeeded_or_failed])
VALUES ('${p_year_month}', '${p_ats_id}', '${p_job_board_id}', '${p_succeeded_or_failed}');