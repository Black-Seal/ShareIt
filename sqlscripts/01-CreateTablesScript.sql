-- Users table
CREATE TABLE [dbo].[Users] (
    [User_ID]   INT IDENTITY(1,1) NOT NULL,  -- Auto-incrementing User_ID
    [FirstName] VARCHAR (255) NOT NULL,
    [LastName]  VARCHAR (255) NOT NULL,
    [Email]     VARCHAR (255) NULL,
    [Address]   VARCHAR (255) NULL,
    [Contact]   VARCHAR (20)  NULL,
    PRIMARY KEY CLUSTERED ([User_ID] ASC),   -- Primary Key on User_ID
    UNIQUE NONCLUSTERED ([Email] ASC)        -- Unique constraint on Email
);

-- Items table
CREATE TABLE [dbo].[Items] (
    [Item_ID]     INT             NOT NULL,
    [User_ID]     INT             NOT NULL,
    [Item_Name]   VARCHAR (255)   NOT NULL,
    [Description] VARCHAR (255)   NULL,
    [Price]       DECIMAL (10, 2) NOT NULL,
    PRIMARY KEY CLUSTERED ([Item_ID] ASC),
    FOREIGN KEY ([User_ID]) REFERENCES [dbo].[Users] ([User_ID])
);

-- Listings table
CREATE TABLE [dbo].[Listings] (
    [Listing_ID]  INT  NOT NULL,
    [Borrower_ID] INT  NOT NULL,
    [Lender_ID]   INT  NOT NULL,
    [Item_ID]     INT  NOT NULL,
    [Start_Date]  DATE DEFAULT (getdate()) NOT NULL,
    [End_Date]    DATE NOT NULL,
    [Return_Flag] BIT  DEFAULT ((0)) NOT NULL,
    PRIMARY KEY CLUSTERED ([Listing_ID] ASC),
    FOREIGN KEY ([Borrower_ID]) REFERENCES [dbo].[Users] ([User_ID]),
    FOREIGN KEY ([Item_ID]) REFERENCES [dbo].[Items] ([Item_ID]),
    FOREIGN KEY ([Lender_ID]) REFERENCES [dbo].[Users] ([User_ID])
);

-- Fines table
CREATE TABLE [dbo].[Fines] (
    [Fine_ID]     INT             NOT NULL,
    [Listing_ID]  INT             NOT NULL,
    [Borrower_ID] INT             NOT NULL,
    [Fine_Amount] DECIMAL (10, 2) NOT NULL,
    [Fine_Date]   DATE            DEFAULT (getdate()) NOT NULL,
    PRIMARY KEY CLUSTERED ([Fine_ID] ASC),
    FOREIGN KEY ([Borrower_ID]) REFERENCES [dbo].[Users] ([User_ID]),
    FOREIGN KEY ([Listing_ID]) REFERENCES [dbo].[Listings] ([Listing_ID])
);
