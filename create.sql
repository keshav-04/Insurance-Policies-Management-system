CREATE TABLE PolicyHolder (
    PolicyHolderID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Policy (
    PolicyID SERIAL PRIMARY KEY,
    PolicyNumber VARCHAR(20) NOT NULL UNIQUE,
    PolicyType VARCHAR(50) NOT NULL,
    CoverageAmount DECIMAL(15, 2) NOT NULL,
    PremiumAmount DECIMAL(10, 2) NOT NULL,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    PolicyHolderID INT REFERENCES PolicyHolder(PolicyHolderID) NOT NULL,
    CompanyID INT REFERENCES InsuranceCompany(CompanyID) NOT NULL,
    AgentID INT REFERENCES Agent(AgentID),
    CoverageTypeID INT REFERENCES CoverageType(CoverageTypeID) NOT NULL
);

CREATE TABLE InsuranceCompany (
    CompanyID SERIAL PRIMARY KEY,
    CompanyName VARCHAR(255) NOT NULL UNIQUE,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Agent (
    AgentID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Address VARCHAR(255),
    PhoneNumber VARCHAR(15) NOT NULL,
    Password VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Claim (
    ClaimID SERIAL PRIMARY KEY,
    PolicyID INT REFERENCES Policy(PolicyID) NOT NULL,
    DateFiled DATE NOT NULL,
    ClaimAmount DECIMAL(15, 2) NOT NULL,
    Status VARCHAR(50) NOT NULL,
    Description TEXT
);

CREATE TABLE Beneficiary (
    BeneficiaryID SERIAL PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    Relationship VARCHAR(50) NOT NULL,
    Percentage DECIMAL(5, 2) NOT NULL
);

CREATE TABLE Payment (
    PaymentID SERIAL PRIMARY KEY,
    ClaimID INT REFERENCES Claim(ClaimID) NOT NULL,
    Amount DECIMAL(15, 2) NOT NULL,
    PaymentDate DATE NOT NULL,
    Method VARCHAR(50) NOT NULL
);

CREATE TABLE CoverageType (
    CoverageTypeID SERIAL PRIMARY KEY,
    CoverageName VARCHAR(255) NOT NULL,
    Description TEXT
);

CREATE TABLE Maturity (
    MaturityID SERIAL PRIMARY KEY,
    PolicyID INT REFERENCES Policy(PolicyID) NOT NULL,
    MaturityDate DATE NOT NULL,
    MaturityAmount DECIMAL(15, 2) NOT NULL
);
