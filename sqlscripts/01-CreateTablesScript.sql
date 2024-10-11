-- Users table
CREATE TABLE [dbo].[users] (
    [UserID]   INT IDENTITY(1,1) NOT NULL,  -- Auto-incrementing UserID
    [FirstName] VARCHAR (255) NOT NULL,
    [LastName]  VARCHAR (255) NOT NULL,
    [Email]     VARCHAR (255) NULL,
    [Address]   VARCHAR (255) NULL,
    [Contact]   VARCHAR (20)  NULL,
    PRIMARY KEY CLUSTERED ([UserID] ASC),    -- Primary Key on UserID
    UNIQUE NONCLUSTERED ([Email] ASC)        -- Unique constraint on Email
);

-- Items table
CREATE TABLE [dbo].[items] (
    [ItemID]     INT             NOT NULL,
    [UserID]     INT             NOT NULL,
    [Item_Name]   VARCHAR (255)   NOT NULL,
    [Description] VARCHAR (255)   NULL,
    [Price]       DECIMAL (10, 2) NOT NULL,
    PRIMARY KEY CLUSTERED ([ItemID] ASC),
    FOREIGN KEY ([UserID]) REFERENCES [dbo].[users] ([UserID])
);

-- Listings table
CREATE TABLE [dbo].[listings] (
    [ListingID]  INT  NOT NULL,
    [BorrowerID] INT  NOT NULL,
    [LenderID]   INT  NOT NULL,
    [ItemID]     INT  NOT NULL,
    [StartDate]  DATE DEFAULT (getdate()) NOT NULL,
    [EndDate]    DATE NOT NULL,
    [ReturnFlag] BIT  DEFAULT ((0)) NOT NULL,
    PRIMARY KEY CLUSTERED ([ListingID] ASC),
    FOREIGN KEY ([BorrowerID]) REFERENCES [dbo].[Users] ([UserID]),
    FOREIGN KEY ([ItemID]) REFERENCES [dbo].[Items] ([ItemID]),
    FOREIGN KEY ([LenderID]) REFERENCES [dbo].[Users] ([UserID])
);

-- Fines table
CREATE TABLE [dbo].[fines] (
    [FineID]     INT             NOT NULL,
    [ListingID]  INT             NOT NULL,
    [BorrowerID] INT             NOT NULL,
    [FineAmount] DECIMAL (10, 2) NOT NULL,
    [FineDate]   DATE            DEFAULT (getdate()) NOT NULL,
    PRIMARY KEY CLUSTERED ([FineID] ASC),
    FOREIGN KEY ([BorrowerID]) REFERENCES [dbo].[users] ([UserID]),
    FOREIGN KEY ([ListingID]) REFERENCES [dbo].[Listings] ([ListingID])
);
