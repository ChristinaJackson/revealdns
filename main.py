import whois
import socket


#using whois for now, will want to move to using rdap in the future,
#with a whois fallback when tld does not support rdap

###TBD - Get DNS Records

def validate_domain(domain_name):
    #check for blank input
    if not domain_name or domain_name.strip() == "":
        return {"is_valid": False, "error": "Domain name cannot be empty"}
    # non-ASCII domains conversion to punycode
    try:
        # Convert Unicode domain to Punycode
        punycode_domain = domain_name.encode("idna").decode("ascii")
        # use dns to check if the domain is valid
        socket.gethostbyname(punycode_domain)
        return {"is_valid": True, "error": None}
    except (socket.gaierror, UnicodeError):
        # general error
        return {"is_valid": False, "error": "Invalid domain name or domain does not resolve"}
    except Exception as e:
        # catch any unexpected errors
        return {"is_valid": False, "error": f"Unexpected error: {str(e)}"}

def get_ipinfo(ip_address):
    try:
        hosting_provider_ip = socket.gethostbyname(ip_address)
        return hosting_provider_ip
    #addressing common errors
    except socket.gaierror as e:
        # handle invalid domain or IP address
        # -2 is eai_noname - host name cannot resolve because does not exist or is invalid
        if e.errno == -2:
            return {"error": "Hostname not found"}
        #-3 is eai_again, temp dns resolution failure
        elif e.errno == -3:
            return {"error": "Temporary DNS issue, try again"}
        else:
            return {"error": f"DNS resolution failed: {e.strerror}"}
    except Exception as e:
        # Catch any other unexpected errors
        return {"error": str(e), "message": "An unexpected error occurred"}

def generate_ipinfo_link(ip_address):
    # Generate IPinfo link
    return f"https://ipinfo.io/{ip_address}"

def get_domain_registrar_info(domain_name):
    # whois lookup, want abuse contact
    domain_registrar = whois.whois(domain_name)

    if all(value is None for value in domain_registrar.values()):
        return {
            "registrar_info": {
                "name": "Not Available",
                "url": "Not Available",
            },
            "abuse_emails": [],
            "other_emails": [],
            "error": "Invalid domain or no registrar data available"
        }

    #registrar urls
    registrar_url = domain_registrar.get("registrar_url")
    registrar_name = domain_registrar.get("registrar")

    #sort and list emails
    emails = domain_registrar.get('emails', [])
    if isinstance(emails, str):  # If 'emails' is a single string
        emails = [emails]  # Convert it to a list

    abuse_emails = [email for email in emails if "abuse" in email.lower()]
    other_emails = [email for email in emails if email not in abuse_emails]
    return {
        "registrar_info": {
            "name": registrar_name or "Not Available",
            "url": registrar_url or "Not Available",
        },
        "abuse_emails": abuse_emails,
        "other_emails": other_emails
    }

#may want to come back and break this up a bit in the future
def get_info(domain_name):
    domain_input = domain_name
    # validate domain input
    validation_result = validate_domain(domain_name)
    if not validation_result["is_valid"]:
        # if its invalid, return error
        return {
            "results for": domain_name,
            "error": validation_result["error"],
            "domain_registrar": None,
            "hosting_provider": None
        }

    domain_registrar = get_domain_registrar_info(domain_name)
    hosting_provider_ip = get_ipinfo(domain_name)
    hosting_provider = {}

    if isinstance(hosting_provider_ip, dict) and "error" in hosting_provider_ip:
        # If there's an error, add the error to the results
        hosting_provider = {
            "ip": None,
            "lookup_url": None,
            "error": hosting_provider_ip["error"]
        }
    else:
        # If no error, create the lookup URL
        ipinfo_url = generate_ipinfo_link(hosting_provider_ip)
        hosting_provider = {
            "ip": hosting_provider_ip,
            "lookup_url": ipinfo_url
        }
    results = {
        "results for": domain_input,
        "domain_registrar": domain_registrar,
        "hosting_provider": hosting_provider
    }
    return results





###TESTING CONTENT#####

#test domains
# www.lukeandlouise.com
# yieldscredit.com
# tabulation.co
# www.holidaypartyevents.com
# sanitär.jetzt

# print(get_ipinfo("example.com"))  # Valid domain
# print(get_ipinfo("invalid-domain"))  # Invalid domain
# print(get_ipinfo(""))  # Empty input

print(get_info('sanitär.jetzt'))

# print(whois.whois(''))

### results structure:
# {
#     "domain_registrar": {
#         "registrar_info": {
#             "name": "Launchpad.com Inc.",
#             "url": "http://www.launchpad.com"
#         },
#         "abuse_emails": ["abuse@hostgator.com"],
#         "other_emails": ["info@crustnation.com", "domain.operations@web.com"]
#     },
#     "hosting_provider": {
#         "ip": "162.214.129.144",
#         "lookup_url": "https://ipinfo.io/162.214.129.144"
#     }
# }

