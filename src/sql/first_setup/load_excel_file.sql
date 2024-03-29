
DECLARE @table NVARCHAR(200);
DECLARE @path NVARCHAR(200);

SET @path = 'c:\PycharmProjects\data_site\files\master_data\ats_job_board.xlsx'
SET @table = 'ats_job_board'

DECLARE @command nvarchar(1000);
DECLARE @command2 nvarchar(1000);


SET @command = N' IF OBJECT_ID(''dbo.' + @table + ''', ''U'') IS NOT NULL ' +
               N'  drop table dbo.' + @table + '; '
EXECUTE (@command);

SET @command2 =  N' SELECT *, GETDATE() as load_date INTO dbo.' + @table +
                N' FROM OPENROWSET(''Microsoft.ACE.OLEDB.12.0'', ' +
                N' ''Excel 12.0;Database='+ @path + ';'' ,'     +
                N' ''SELECT * FROM [Sheet1$]'')'
EXECUTE (@command2);