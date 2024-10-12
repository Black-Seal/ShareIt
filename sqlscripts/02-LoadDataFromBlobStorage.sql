CREATE DATABASE SCOPED CREDENTIAL MyCredential
WITH IDENTITY = 'SHARED ACCESS SIGNATURE', 
SECRET = 'sp=r&st=2024-10-12T10:45:31Z&se=2024-10-12T18:45:31Z&spr=https&sv=2022-11-02&sr=c&sig=5f6kjfGDlCLj9BtNOS9FiLFgN1QAw8GSzH%2BDz8DXFN8%3D';
GO

CREATE EXTERNAL DATA SOURCE ShareIt_Datalake
WITH(
    TYPE = BLOB_STORAGE,
    LOCATION = 'https://shareitblobstorage.blob.core.windows.net/shareit-blob',
    CREDENTIAL = MyCredential
);
GO

BULK INSERT dbo.users
FROM 'users.csv'
WITH (
    DATA_SOURCE = 'ShareIt_Datalake',
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

BULK INSERT dbo.items
FROM 'items.csv'
WITH (
    DATA_SOURCE = 'ShareIt_Datalake',
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO

BULK INSERT dbo.listings
FROM 'listings.csv'
WITH (
    DATA_SOURCE = 'ShareIt_Datalake',
    FORMAT = 'CSV',
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);
GO
