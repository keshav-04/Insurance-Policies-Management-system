-- Readme 
-- Triggers - 
-- .policy_dates_trigger
-- claim_amount_trigger
-- beneficiary_percentages_trigger
-- maturity_date_trigger
-- update_policy_holder_trigger
-- update_claim_status_trigger
-- terminate_policy_trigger
-- deny_claim_trigger
-- auto_approve_claim_trigger
-- .renew_policy_trigger
-- .update_claim_amount_trigger

-- 1. Policy Insertion:
-- Ensures that the end date of a policy is greater than the start date.

CREATE OR REPLACE FUNCTION validate_policy_dates()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.StartDate >= NEW.EndDate THEN
        RAISE EXCEPTION 'End date must be greater than start date';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER policy_dates_trigger
BEFORE INSERT OR UPDATE ON Policy
FOR EACH ROW
EXECUTE FUNCTION validate_policy_dates();

-- 2. Claim Amount Validation:
-- Ensures that the claimed amount is less than or equal to the coverage amount of the associated policy.

CREATE OR REPLACE FUNCTION validate_claim_amount()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.ClaimAmount > (SELECT CoverageAmount FROM Policy WHERE PolicyID = NEW.PolicyID) THEN
        RAISE EXCEPTION 'Claim amount exceeds policy coverage';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER claim_amount_trigger
BEFORE INSERT ON Claim
FOR EACH ROW
EXECUTE FUNCTION validate_claim_amount();

-- 3. Beneficiary Percentage Validation:
-- Ensures that the sum of beneficiary percentages for a policy does not exceed 100%.
CREATE OR REPLACE FUNCTION validate_beneficiary_percentages()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT SUM(Percentage) FROM Beneficiary WHERE PolicyID = NEW.PolicyID) + NEW.Percentage > 100 THEN
        RAISE EXCEPTION 'Beneficiary percentages exceed 100% for the policy';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER beneficiary_percentages_trigger
BEFORE INSERT ON Beneficiary
FOR EACH ROW
EXECUTE FUNCTION validate_beneficiary_percentages();

-- 4. Maturity Date Validation:
-- Ensures that the maturity date is within the policy's start and end date.
CREATE OR REPLACE FUNCTION validate_maturity_date()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.MaturityDate < (SELECT StartDate FROM Policy WHERE PolicyID = NEW.PolicyID)
        OR NEW.MaturityDate > (SELECT EndDate FROM Policy WHERE PolicyID = NEW.PolicyID) THEN
        RAISE EXCEPTION 'Maturity date must be within the policy start and end date';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER maturity_date_trigger
BEFORE INSERT ON Maturity
FOR EACH ROW
EXECUTE FUNCTION validate_maturity_date();

-- 5. Cascading Policy Holder Update:
CREATE OR REPLACE FUNCTION update_policy_holder_details()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Policy SET
        FirstName = NEW.FirstName,
        LastName = NEW.LastName,
        Address = NEW.Address,
        PhoneNumber = NEW.PhoneNumber,
        Email = NEW.Email
    WHERE Policy.PolicyHolderID = NEW.PolicyHolderID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_policy_holder_trigger
AFTER UPDATE ON PolicyHolder
FOR EACH ROW
EXECUTE FUNCTION update_policy_holder_details();

--  6. Claim Status Update:
CREATE OR REPLACE FUNCTION update_claim_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Status = 'Approved' AND (SELECT COALESCE(SUM(Amount), 0) FROM Payment WHERE ClaimID = NEW.ClaimID) < NEW.ClaimAmount THEN
        RAISE EXCEPTION 'Claim cannot be approved without sufficient payments';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_claim_status_trigger
BEFORE UPDATE ON Claim
FOR EACH ROW
EXECUTE FUNCTION update_claim_status();

-- 7. Policy Termination:
CREATE OR REPLACE FUNCTION terminate_policy()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.EndDate < CURRENT_DATE THEN
        UPDATE Policy SET
            EndDate = CURRENT_DATE
        WHERE Policy.PolicyID = NEW.PolicyID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER terminate_policy_trigger
BEFORE UPDATE ON Policy
FOR EACH ROW
EXECUTE FUNCTION terminate_policy();

-- 8. Claim Denial:
CREATE OR REPLACE FUNCTION deny_claim()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Status = 'Denied' AND (SELECT COALESCE(SUM(Amount), 0) FROM Payment WHERE ClaimID = NEW.ClaimID) > 0 THEN
        RAISE EXCEPTION 'Denied claim cannot have associated payments';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER deny_claim_trigger
BEFORE UPDATE ON Claim
FOR EACH ROW
EXECUTE FUNCTION deny_claim();

-- 9. Automatic Claim Approval:
CREATE OR REPLACE FUNCTION auto_approve_claim()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.Status = 'Submitted' AND (SELECT COALESCE(SUM(Amount), 0) FROM Payment WHERE ClaimID = NEW.ClaimID) >= NEW.ClaimAmount * 0.8 THEN
        UPDATE Claim SET
            Status = 'Approved'
        WHERE Claim.ClaimID = NEW.ClaimID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER auto_approve_claim_trigger
BEFORE UPDATE ON Claim
FOR EACH ROW
EXECUTE FUNCTION auto_approve_claim();


-- 10. Policy Renewal:
CREATE OR REPLACE FUNCTION renew_policy()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.EndDate < CURRENT_DATE THEN
        UPDATE Policy SET
            StartDate = CURRENT_DATE,
            EndDate = CURRENT_DATE + INTERVAL '1 year'
        WHERE Policy.PolicyID = NEW.PolicyID;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER renew_policy_trigger
BEFORE UPDATE ON Policy
FOR EACH ROW
EXECUTE FUNCTION renew_policy();

-- 11. update_claim_amount after payment
CREATE OR REPLACE FUNCTION update_claim_amount()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE Claim SET
        ClaimAmount = ClaimAmount - NEW.Amount
    WHERE Claim.ClaimID = NEW.ClaimID;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_claim_amount_trigger
AFTER INSERT ON Payment
FOR EACH ROW
EXECUTE FUNCTION update_claim_amount();

