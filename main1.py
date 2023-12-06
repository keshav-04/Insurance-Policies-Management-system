import psycopg2
from psycopg2 import sql
import bcrypt

user = {
    'id': '',
    'first_name': '',
    'last_name': '',
    'address': '',    
    'phone': '',
    'password': '',
    'email': '',
}

company = {
    'id': '',
    'name': '',
    'address': '',
    'phone': '',
    'password': '',
    'email': '',
}

def userClear():
    user['id'] = ''
    user['first_name'] = ''
    user['last_name'] = ''
    user['address'] = ''    
    user['phone'] = ''
    user['password'] = ''
    user['email'] = ''


def companyClear():
    company['id'] = ''
    company['name'] = ''
    company['address'] = ''
    company['phone'] = ''
    company['password'] = ''
    company['email'] = ''

logged_in = 0
email = ''
password = ''



# Hash password
# hash_password = lambda password: bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
def hash_password(password):
    return password

# Check password
# check_password = lambda password, hashed_password: bcrypt.checkpw(password.encode('utf-8'), hashed_password)
def check_password(password, hashed_password):
    return password == hashed_password

def agent_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    try:
        c.execute("SELECT Password, AgentID FROM Agent WHERE Email = %s", (email,))
        result = c.fetchone()
        if result == None:
            print("No such user exists. Please register.")
            return
        if check_password(password, result[0]):
            print("Login successful")
            c.execute("SELECT * FROM Agent WHERE AgentID = %s", (result[1],))
            result = c.fetchone()
            user['id'] = result[0]
            user['first_name'] = result[1]
            user['last_name'] = result[2]
            user['address'] = result[3]
            user['phone'] = result[4]
            user['password'] = result[5]
            user['email'] = result[6]
            return True
        
        else:
            print("Incorrect password. Please try again.")
            return False
    
    except psycopg2.Error as e:
        print(e)
        return
    
def agent_register():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone number: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    hashed_password = hash_password(password)
    try:
        c.execute("INSERT INTO Agent (FirstName, LastName, Address, PhoneNumber, Password, Email) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, address, phone, hashed_password, email))
        conn.commit()
        print("Registration successful")
    except psycopg2.Error as e:
        print(e)
        return
        
    return True


def policyHolder_login():
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    c.execute("SELECT Password, PolicyHolderID FROM PolicyHolder WHERE Email = %s", (email,))
    result = c.fetchone()
    if result == None:
        print("No such user exists. Please register.")
        return False
    if check_password(password, result[0]):
        print("Login successful")
        logged_in = 2
        c.execute("SELECT * FROM PolicyHolder WHERE PolicyHolderID = %s", (result[1],))
        result = c.fetchone()
        user['id'] = result[0]
        user['first_name'] = result[1]
        user['last_name'] = result[2]
        user['address'] = result[3]
        user['phone'] = result[4]
        user['password'] = result[5]
        user['email'] = result[6]
        return True
    
    else:
        print("Incorrect password. Please try again.")
        return
    
def policyHolder_register():
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    address = input("Enter your address: ")
    phone = input("Enter your phone number: ")
    password = input("Enter your password: ")
    email = input("Enter your email: ")
    hashed_password = hash_password(password)
    c.execute("INSERT INTO PolicyHolder (FirstName, LastName, Address, PhoneNumber, Password, Email) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, address, phone, hashed_password, email))
    conn.commit()
    print("Registration successful")
    return True


# Connecting to the database
conn = psycopg2.connect(
    database="project",
    user="postgres",
    password="keshav04",
    host="localhost",
    port="5432"
)
if(conn):
    print("Connection to database successful")


c = conn.cursor()


while True:
    if logged_in == 0:
        userClear()
        companyClear()

        print("Enter the role:")
        print("1. Agent")
        print("2. Customer")
        print("3. Insurance Company")
        print("0. Exit")

        role = input("Enter the option number: ")

        # Agent
        if role == "1":
            c1 = input("Login or Register (l/r): ")
            if c1 == "l":
                if(agent_login()):
                    logged_in = 1
                else:
                    continue
            elif c1 == "r":
                agent_register()
            else:
                print("Invalid option. Exiting.")
                continue
        
        # Customer
        elif role == "2":
            c2 = input("Login or Register (l/r): ")
            if c2 == "l":
                if(policyHolder_login()):
                    logged_in = 2
            elif c2 == "r":
                policyHolder_register()
            else:
                print("Invalid option. Exiting.")
                continue

        # Insurance Company
        elif role == "3":
            c3 = input("Login or Register (l/r): ")
            if c3 == "l":
                name = input("Enter Company name: ")
                password = input("Enter your password: ")
                c.execute("SELECT Password FROM InsuranceCompany WHERE CompanyName = %s", (name,))
                result = c.fetchone()
                if result == None:
                    print("No such user exists. Please register.")
                    continue
                if check_password(password, result[0]):
                    print("Login successful")
                    logged_in = 3
                    c.execute("SELECT * FROM InsuranceCompany WHERE Name = %s", (name,))
                    result = c.fetchone()
                    company['id'] = result[0]
                    company['name'] = result[1]
                    company['address'] = result[2]
                    company['phone'] = result[3]
                    company['password'] = result[4]
                    company['email'] = result[5]
                else:
                    print("Incorrect password. Please try again.")

            elif c3 == "r":
                name = input("Enter Company name: ")
                address = input("Enter your address: ")
                phone = input("Enter your phone number: ")
                password = input("Enter your password: ")
                email = input("Enter your email: ")
                hashed_password = hash_password(password)
                try:
                    c.execute("INSERT INTO InsuranceCompany (CompanyName, Address, PhoneNumber, Password, Email) VALUES (%s, %s, %s, %s, %s)", (name, address, phone, hashed_password, email))
                    conn.commit()
                    print("Registration successful")
                except psycopg2.Error as e:
                    print(e)
                    continue
                logged_in = 3
                c.execute("SELECT * FROM InsuranceCompany WHERE CompanyName = %s", (name,))
                result = c.fetchone()
                company['id'] = result[0]
                company['name'] = result[1]
                company['address'] = result[2]
                company['phone'] = result[3]
                company['password'] = result[4]
                company['email'] = result[5]
            else:
                print("Invalid option. Exiting.")
                continue

        # Exit
        elif role == "0":
            break

        else:
            print("Invalid option. Exiting.")
            continue

    elif logged_in == 1:
        print("Enter the option number:")
        print("1. View all policies")
        print("2. Add a new policy")
        print("3. Add a new claim")
        print("4. Add a new policy holder")
        print("5. Update and renew policy")
        print("6. Update a claim")
        print("7. Update a policy holder")
        print("8. Delete a policy")
        print("9. Delete a claim")
        print("10. Delete a policy holder")
        print("11. Check mature policies")
        print("12. Add a coverage type")
        print("13. Calculate premium for a policy")

             
        print("0. Exit")

        option = input("Enter the option number: ")

        # View all policies
        if option == "1":
            c.execute("SELECT * FROM Policy")
            result = c.fetchall()
            print(result)
        
        
        # Add a new policy
        elif option == "2":
            policy_number = input("Enter the policy number: ")
            policy_type = input("Enter the policy type: ")
            coverage_amount = input("Enter the coverage amount: ")
            premium_amount = input("Enter the premium amount: ")
            start_date = input("Enter the start date: ")
            end_date = input("Enter the end date: ")
            policy_holder_id = input("Enter the policy holder id: ")
            company_id = input("Enter the company id: ")
            coverage_id = input("Enter the coverage type id: ")
            try:
                c.execute("INSERT INTO Policy (PolicyNumber, PolicyType, CoverageAmount, PremiumAmount, StartDate, EndDate, PolicyHolderID, CompanyID, AgentID, CoverageTypeID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (policy_number, policy_type, coverage_amount, premium_amount, start_date, end_date, policy_holder_id, company_id, user["id"], coverage_id))
                conn.commit()
                print("Policy added successfully")
            except psycopg2.Error as e:
                print(e)
                continue
        
        # Add a new claim
        elif option == "3":
            claim_amount = input("Enter the claim amount: ")
            status = input("Enter the status: ")
            description = input("Enter the description: ")
            policy_id = input("Enter the policy id: ")
            date = input("Enter the date: ")
            try:
                c.execute("INSERT INTO Claim (ClaimAmount, Status, Description, PolicyID, DateFiled) VALUES (%s, %s, %s, %s, %s)", (claim_amount, status, description, policy_id, date))
                conn.commit()
                print("Claim added successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Add a new policy holder
        elif option == "4":
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            address = input("Enter the address: ")
            phone = input("Enter the phone number: ")
            password = input("Enter the password: ")
            email = input("Enter the email: ")
            try:
                c.execute("INSERT INTO PolicyHolder (FirstName, LastName, Address, PhoneNumber, Password, Email) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, address, phone, password, email))
                conn.commit()
                print("Policy holder added successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Update and renew policy
        elif option == "5":
            policy_holder_id = input("Enter the policy holder id: ")
            policy_id = input("Enter the policy id: ")

            c.execute("SELECT * FROM Policy WHERE PolicyID = %s AND PolicyHolderID = %s", (policy_id, policy_holder_id))
            result = c.fetchone()
            if result == None:
                print("No such policy exists for the policy holder under your name")
                continue

            new_coverage_amount = input("Enter the new coverage amount: ")
            new_premium_amount = input("Enter the new premium amount: ")

            try:
                c.execute("UPDATE Policy SET CoverageAmount = %s, PremiumAmount = %s WHERE PolicyID = %s", (new_coverage_amount, new_premium_amount, policy_id))
                conn.commit()
                print("Policy updated successfully")
            except psycopg2.Error as e:
                print(e)
                continue

            c.execute("SELECT * FROM Policy WHERE PolicyID = %s", (policy_id,))
            result = c.fetchone()
            if result[6] < result[7]:
                print("Policy renewed successfully")
            else:
                print("Policy cannot be renewed")

        # Update a claim
        elif option == "6":
            claim_id = input("Enter the claim id: ")
            policy_holder_id = input("Enter the policy holder id: ")

            c.execute("SELECT * FROM Claim WHERE ClaimID = %s AND PolicyID IN (SELECT PolicyID FROM Policy WHERE PolicyHolderID = %s)", (claim_id, policy_holder_id))
            result = c.fetchone()
            if result == None:
                print("No such claim exists for the policy holder under your name")
                continue

            new_status = input("Enter the new status: ")
            new_description = input("Enter the new description: ")

            try:
                c.execute("UPDATE Claim SET Status = %s, Description = %s WHERE ClaimID = %s", (new_status, new_description, claim_id))
                conn.commit()
                print("Claim updated successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Update a policy holder
        elif option == "7":
            policy_holder_id = input("Enter the policy holder id: ")

            c.execute("SELECT * FROM PolicyHolder WHERE PolicyHolderID = %s", (policy_holder_id,))
            result = c.fetchone()
            if result == None:
                print("No such policy holder exists")
                continue

            ch = input("Update (a)ll or (s)pecific fields: ")
            if ch == "a":
                new_first_name = input("Enter the new first name: ")
                new_last_name = input("Enter the new last name: ")
                new_address = input("Enter the new address: ")
                new_phone = input("Enter the new phone number: ")
                new_password = input("Enter the new password: ")
                new_email = input("Enter the new email: ")

                try:
                    c.execute("UPDATE PolicyHolder SET FirstName = %s, LastName = %s, Address = %s, PhoneNumber = %s, Password = %s, Email = %s WHERE PolicyHolderID = %s", (new_first_name, new_last_name, new_address, new_phone, new_password, new_email, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                except psycopg2.Error as e:
                    print(e)
                    continue
            
            elif ch == "s":
                print("Enter the field to update:")
                print("1. First Name")
                print("2. Last Name")
                print("3. Address")
                print("4. Phone Number")
                print("5. Password")
                print("6. Email")

                field = input("Enter the option number: ")
                if field == "1":
                    new_first_name = input("Enter the new first name: ")
                    c.execute("UPDATE PolicyHolder SET FirstName = %s WHERE PolicyHolderID = %s", (new_first_name, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                elif field == "2":
                    new_last_name = input("Enter the new last name: ")
                    c.execute("UPDATE PolicyHolder SET LastName = %s WHERE PolicyHolderID = %s", (new_last_name, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                elif field == "3":
                    new_address = input("Enter the new address: ")
                    c.execute("UPDATE PolicyHolder SET Address = %s WHERE PolicyHolderID = %s", (new_address, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                elif field == "4":
                    new_phone = input("Enter the new phone number: ")
                    c.execute("UPDATE PolicyHolder SET PhoneNumber = %s WHERE PolicyHolderID = %s", (new_phone, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                elif field == "5":
                    new_password = input("Enter the new password: ")

                    hashed_password = hash_password(new_password)
                    c.execute("UPDATE PolicyHolder SET Password = %s WHERE PolicyHolderID = %s", (hashed_password, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                elif field == "6":
                    new_email = input("Enter the new email: ")
                    c.execute("UPDATE PolicyHolder SET Email = %s WHERE PolicyHolderID = %s", (new_email, policy_holder_id))
                    conn.commit()
                    print("Policy holder updated successfully")
                else:
                    print("Invalid option. Exiting.")
                    continue
            else:
                print("Invalid option. Exiting.")
                continue

        # Delete a policy
        elif option == "8":
            policy_id = input("Enter the policy id: ")
            policy_holder_id = input("Enter the policy holder id: ")

            c.execute("SELECT * FROM Policy WHERE PolicyID = %s AND PolicyHolderID = %s", (policy_id, policy_holder_id))
            result = c.fetchone()
            if result == None:
                print("No such policy exists for the policy holder under your name")
                continue
            
            try:
                c.execute("DELETE FROM Policy WHERE PolicyID = %s", (policy_id,))
                conn.commit()
                print("Policy deleted successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Delete a claim
        elif option == "9":
            claim_id = input("Enter the claim id: ")
            policy_holder_id = input("Enter the policy holder id: ")

            c.execute("SELECT * FROM Claim WHERE ClaimID = %s AND PolicyID IN (SELECT PolicyID FROM Policy WHERE PolicyHolderID = %s)", (claim_id, policy_holder_id))
            result = c.fetchone()
            if result == None:
                print("No such claim exists for the policy holder under your name")
                continue
            
            try:
                c.execute("DELETE FROM Claim WHERE ClaimID = %s", (claim_id,))
                conn.commit()
                print("Claim deleted successfully")
            except psycopg2.Error as e:
                print(e)
                continue
        
        # Delete a policy holder
        elif option == "10":
            policy_holder_id = input("Enter the policy holder id: ")

            c.execute("SELECT * FROM PolicyHolder WHERE PolicyHolderID = %s", (policy_holder_id,))
            result = c.fetchone()
            if result == None:
                print("No such policy holder exists")
                continue

            try:
                c.execute("DELETE FROM PolicyHolder WHERE PolicyHolderID = %s", (policy_holder_id,))
                conn.commit()
                print("Policy holder deleted successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Check Mature Policies
        elif option == "11":
            c.execute("SELECT * FROM Policy WHERE EndDate < CURRENT_DATE")
            result = c.fetchall()
            print(result)

        # Add a coverage type
        elif option == "12":
            coverage_name = input("Enter the coverage name: ")
            description = input("Enter the description: ")
            try:
                c.execute("INSERT INTO CoverageType (CoverageName, Description) VALUES (%s, %s)", (coverage_name, description))
                conn.commit()
                print("Coverage type added successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Calculate premium for a policy
        elif option == "13":
            policy_id = input("Enter the policy id: ")
            try:   
                c.execute("SELECT calculate_premium(%s)", (policy_id,))
                result = c.fetchone()
                print(result)
            except psycopg2.Error as e:
                print(e)
                continue

        # Exit
        elif option == "0":
            logged_in = 0
            continue

        else:
            print("Invalid option. Exiting.")
            continue

    elif logged_in == 2:
        print("Enter the option number:")
        print("1. View all policies")
        print("2. Check remaining coverage of a policy")
        print("3. Check policy status")
        print("4. make a claim")
        print("5. Calculate total payments for a claim")
        print("6. Made a payment for a claim")
        print("7. Add a new beneficiary")
        print("8. Calculate beneficiary payout")
        print("9. Check payment due date")
        print("10. Calculate premium for a policy")

        print("0. Exit")

        option = input("Enter the option number: ")

        # View all policies
        if option == "1":
            c.execute("SELECT * FROM Policy WHERE PolicyHolderID = %s", (user['id'],))
            result = c.fetchall()
            print(result)

        # Check remaining coverage of a policy
        elif option == "2":
            policy_id = input("Enter the policy id: ")
            c.execute("SELECT calculate_remaining_coverage(%s)", (policy_id,))
            result = c.fetchone()
            print(result)
        
        # Check policy status
        elif option == "3":
            policy_id = input("Enter the policy id: ")
            c.execute("SELECT check_policy_status(%s)", (policy_id,))
            result = c.fetchone()
            print(result)

        # Make a claim
        elif option == "4":
            policy_id = input("Enter the policy id: ")
            claim_amount = input("Enter the claim amount: ")
            description = input("Enter the description: ")
            c.execute("INSERT INTO Claim (PolicyID, ClaimAmount, Status, Description) VALUES (%s, %s, 'Submitted', %s)", (policy_id, claim_amount, description))
            conn.commit()
            print("Claim submitted successfully")
        

        # Calculate total payments for a claim
        elif option == "5":
            claim_id = input("Enter the claim id: ")
            c.execute("SELECT get_total_payments(%s)", (claim_id,))
            result = c.fetchone()
            print(result)

        # Made a payment for a claim
        elif option == "6":
            claim_id = input("Enter the claim id: ")
            amount = input("Enter the amount: ")
            method = input("Enter the method: ")
            c.execute("INSERT INTO Payment (ClaimID, Amount, PaymentDate, Method) VALUES (%s, %s, CURRENT_DATE, %s)", (claim_id, amount, method))
            conn.commit()
            print("Payment made successfully")

            
        # Add a new beneficiary
        elif option == "7":
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            relationship = input("Enter the relationship: ")
            percentage = input("Enter the percentage: ")
            try:
                c.execute("INSERT INTO Beneficiary (FirstName, LastName, Relationship, Percentage) VALUES (%s, %s, %s, %s)", (first_name, last_name, relationship, percentage))
                conn.commit()
                print("Beneficiary added successfully")
            except psycopg2.Error as e:
                print(e)
                continue

        # Calculate beneficiary payout
        elif option == "8":
            policy_id = input("Enter the policy id: ")
            claim_id = input("Enter the claim id: ")
            beneficiary_id = input("Enter the beneficiary id: ")
            c.execute("SELECT Percentage FROM Beneficiary WHERE BeneficiaryID = %s", (beneficiary_id,))
            result = c.fetchone()

            if result == None:
                print("No such beneficiary exists")
                continue

            beneficiary_percentage = result[0]
            c.execute("SELECT calculate_beneficiary_payout(%s, %s, %s)", (policy_id, claim_id, beneficiary_percentage))
            result = c.fetchone()
            print(result)

        # Check payment due date
        elif option == "9":
            claim_id = input("Enter the claim id: ")
            c.execute("SELECT calculate_payment_due_date(%s)", (claim_id,))
            result = c.fetchone()
            print(result)

        # Calculate premium for a policy
        # elif option == "10":
        #     policy_id = input("Enter the policy id: ")
        #     try:
        #         c.execute("SELECT calculate_premium(%s)", (policy_id,))
        #         result = c.fetchone()
        #         print(result)
        #     except psycopg2.Error as e:
        #         print(e)
        #         continue

        # Exit
        elif option == "0":
            logged_in = 0
            continue

        else:
            print("Invalid option. Exiting.")
            continue

    elif logged_in == 3:
        print("Enter the option number:")
        print("1. Add a new agent")
        print("2. Update an agent")
        print("3. Delete an agent")
        print("0. Exit")

        option = input("Enter the option number: ")

        # Add a new agent
        if option == "1":
            first_name = input("Enter the first name: ")
            last_name = input("Enter the last name: ")
            address = input("Enter the address: ")
            phone = input("Enter the phone number: ")
            password = input("Enter the password: ")
            email = input("Enter the email: ")
            c.execute("INSERT INTO Agent (FirstName, LastName, Address, PhoneNumber, Password, Email) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, address, phone, password, email))
            conn.commit()
            print("Agent added successfully")

        # Update an agent
        elif option == "2":
            agent_id = input("Enter the agent id: ")

            c.execute("SELECT * FROM Agent WHERE AgentID = %s", (agent_id,))
            result = c.fetchone()
            if result == None:
                print("No such agent exists")
                continue

            ch = input("Update (a)ll or (s)pecific fields: ")
            if ch == "a":
                new_first_name = input("Enter the new first name: ")
                new_last_name = input("Enter the new last name: ")
                new_address = input("Enter the new address: ")
                new_phone = input("Enter the new phone number: ")
                new_password = input("Enter the new password: ")
                new_email = input("Enter the new email: ")

                c.execute("UPDATE Agent SET FirstName = %s, LastName = %s, Address = %s, PhoneNumber = %s, Password = %s, Email = %s WHERE AgentID = %s", (new_first_name, new_last_name, new_address, new_phone, new_password, new_email, agent_id))
                conn.commit()
                print("Agent updated successfully")
            
            elif ch == "s":
                print("Enter the field to update:")
                print("1. First Name")
                print("2. Last Name")
                print("3. Address")
                print("4. Phone Number")
                print("5. Password")
                print("6. Email")

                field = input("Enter the option number: ")
                if field == "1":
                    new_first_name = input("Enter the new first name: ")
                    c.execute("UPDATE Agent SET FirstName = %s WHERE AgentID = %s", (new_first_name, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                elif field == "2":
                    new_last_name = input("Enter the new last name: ")
                    c.execute("UPDATE Agent SET LastName = %s WHERE AgentID = %s", (new_last_name, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                elif field == "3":
                    new_address = input("Enter the new address: ")
                    c.execute("UPDATE Agent SET Address = %s WHERE AgentID = %s", (new_address, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                elif field == "4":
                    new_phone = input("Enter the new phone number: ")
                    c.execute("UPDATE Agent SET PhoneNumber = %s WHERE AgentID = %s", (new_phone, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                elif field == "5":
                    new_password = input("Enter the new password: ")

                    hashed_password = hash_password(new_password)
                    c.execute("UPDATE Agent SET Password = %s WHERE AgentID = %s", (hashed_password, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                elif field == "6":
                    new_email = input("Enter the new email: ")
                    c.execute("UPDATE Agent SET Email = %s WHERE AgentID = %s", (new_email, agent_id))
                    conn.commit()
                    print("Agent updated successfully")
                else:
                    print("Invalid option. Exiting.")
                    continue
            else:
                print("Invalid option. Exiting.")
                continue

        # Delete an agent
        elif option == "3":
            agent_id = input("Enter the agent id: ")

            c.execute("SELECT * FROM Agent WHERE AgentID = %s", (agent_id,))
            result = c.fetchone()
            if result == None:
                print("No such agent exists")
                continue

            c.execute("DELETE FROM Agent WHERE AgentID = %s", (agent_id,))
            conn.commit()
            print("Agent deleted successfully")




        # Exit
        elif option == "0":
            logged_in = 0
            continue

        else:
            print("Invalid option. Exiting.")
            continue




conn.close()

