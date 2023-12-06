-- Helper Functions for the Project

-- Calculate Remaining Coverage:
-- Check Policy Status:
-- Get Total Payments for a Claim:
-- Calculate Beneficiary Payout:
-- Calculate Policy Duration:
-- Check Policy Holder Age:
-- Calculate Premium for a Policy:
-- Calculate Payment Due Date:


-- Calculate Remaining Coverage:
CREATE OR REPLACE FUNCTION calculate_remaining_coverage(policy_id INT)
RETURNS DECIMAL(15, 2) AS $$
DECLARE
    total_claimed DECIMAL(15, 2);
BEGIN
    total_claimed := COALESCE((SELECT SUM(ClaimAmount) FROM Claim WHERE PolicyID = policy_id), 0);
    RETURN (SELECT CoverageAmount FROM Policy WHERE PolicyID = policy_id) - total_claimed;
END;
$$ LANGUAGE plpgsql;

-- Check Policy Status:
CREATE OR REPLACE FUNCTION check_policy_status(policy_id INT)
RETURNS VARCHAR(20) AS $$
BEGIN
    RETURN CASE
        WHEN CURRENT_DATE < (SELECT StartDate FROM Policy WHERE PolicyID = policy_id) THEN 'Not Started'
        WHEN CURRENT_DATE > (SELECT EndDate FROM Policy WHERE PolicyID = policy_id) THEN 'Expired'
        ELSE 'Active'
    END;
END;
$$ LANGUAGE plpgsql;


-- Get Total Payments for a Claim:
CREATE OR REPLACE FUNCTION get_total_payments(claim_id INT)
RETURNS DECIMAL(15, 2) AS $$
BEGIN
    RETURN COALESCE((SELECT SUM(Amount) FROM Payment WHERE ClaimID = claim_id), 0);
END;
$$ LANGUAGE plpgsql;

-- Calculate Beneficiary Payout:
CREATE OR REPLACE FUNCTION calculate_beneficiary_payout(policy_id INT, claim_id INT, beneficiary_percentage DECIMAL(5, 2))
RETURNS DECIMAL(15, 2) AS $$
BEGIN
    RETURN (SELECT ClaimAmount FROM Claim WHERE ClaimID = claim_id) * beneficiary_percentage / 100.0;
END;
$$ LANGUAGE plpgsql;


-- Calculate Policy Duration:
CREATE OR REPLACE FUNCTION calculate_policy_duration(policy_id INT)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(MONTH FROM (SELECT EndDate FROM Policy WHERE PolicyID = policy_id) - (SELECT StartDate FROM Policy WHERE PolicyID = policy_id));
END;
$$ LANGUAGE plpgsql;

-- Check Policy Holder Age:
CREATE OR REPLACE FUNCTION check_policy_holder_age(policy_holder_id INT)
RETURNS INTEGER AS $$
BEGIN
    RETURN EXTRACT(YEAR FROM AGE(CURRENT_DATE, (SELECT BirthDate FROM PolicyHolder WHERE PolicyHolderID = policy_holder_id)));
END;
$$ LANGUAGE plpgsql;


-- Calculate Premium for a Policy:
CREATE OR REPLACE FUNCTION calculate_premium(policy_id INT)
RETURNS DECIMAL(10, 2) AS $$
DECLARE
    base_premium DECIMAL(10, 2);
BEGIN
    base_premium := (SELECT PremiumAmount FROM Policy WHERE PolicyID = policy_id);
    RETURN CASE
        WHEN check_policy_holder_age((SELECT PolicyHolderID FROM Policy WHERE PolicyID = policy_id)) < 25 THEN base_premium * 1.2
        WHEN calculate_policy_duration(policy_id) > 12 THEN base_premium * 1.1
        ELSE base_premium
    END;
END;
$$ LANGUAGE plpgsql;


-- Calculate Payment Due Date:
CREATE OR REPLACE FUNCTION calculate_payment_due_date(claim_id INT)
RETURNS DATE AS $$
BEGIN
    RETURN (SELECT DateFiled FROM Claim WHERE ClaimID = claim_id) + INTERVAL '30 days';
END;
$$ LANGUAGE plpgsql;
