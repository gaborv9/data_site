INSERT INTO dbo.scrape_log ([year_month], [ats_id], [job_board_id], [succeeded_or_failed])
VALUES ('${year_month}', '${ats_id}', '${job_board_id}', '${succeeded_or_failed}');