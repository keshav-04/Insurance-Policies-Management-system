# Insurance-Policies-Management-system

# Entities:

1. Policy Holder
    PolicyHolderID (PK)
    FirstName
    LastName
    Address
    PhoneNumber
    Email

2. Policy
    PolicyID (PK)
    PolicyNumber
    PolicyType
    CoverageAmount
    PremiumAmount
    StartDate
    EndDate

3. Insurance Company
    CompanyID (PK)
    CompanyName
    Address
    PhoneNumber
    Email

4. Agent
    AgentID (PK)
    FirstName
    LastName
    Address
    PhoneNumber
    Email

5. Claim
    ClaimID (PK)
    PolicyID (FK)
    DateFiled
    ClaimAmount
    Status
    Description

6. Beneficiary
    BeneficiaryID (PK)
    FirstName
    LastName
    Relationship
    Percentage

7. Payment
    PaymentID (PK)
    ClaimID (FK)
    Amount
    PaymentDate
    Method

8. Coverage Type
    CoverageTypeID (PK)
    CoverageName
    Description

9. Maturity
    MaturityID (PK)
    PolicyID (FK)
    MaturityDate
    MaturityAmount


# Relationships:

Policy Holder (1) ----< Owns >---- (1 or many) Policy
Policy (1) ----< Issued by >---- (1) Insurance Company
Policy (1) ----< Managed by >---- (0 or 1) Agent
Policy (1) ----< Has >---- (1) Coverage Type
Policy (1) ----< Has >---- (0 or many) Beneficiary
Policy (1) ----< Matures >---- (1) Maturity
Claim (1) ----< Belongs to >---- (1) Policy
Claim (1) ----< Filed by >---- (1) Policy Holder
Claim (1) ----< Managed by >---- (0 or 1) Agent
Claim (1) ----< Has >---- (0 or many) Payment
Beneficiary (1) ----< Receives >---- (0 or many) Payment
Agent (0 or 1) ----< Manages >---- (1) Policy Holder
