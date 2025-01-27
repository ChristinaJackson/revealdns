import whois
import socket

#### TODOS
#want to include dns records in initial results
#using whois for now, will want to move to using rdap in the future,
#with a whois fallback when tld does not support rdap
#might be good to cache results

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

def get_ipinfo(domain_name):
    try:
        # Attempt to resolve the domain
        hosting_provider_ip = socket.gethostbyname(domain_name)
        # print(hosting_provider_ip)
        return {"ip": hosting_provider_ip, "error": None}
    except socket.gaierror as e:
        if e.errno == -2:  # Hostname not found
            return {"ip": None, "error": "Hostname not found"}
        elif e.errno == -3:  # Temporary DNS failure
            return {"ip": None, "error": "Temporary DNS issue, try again"}
        else:
            return {"ip": None, "error": f"DNS resolution failed: {e.strerror}"}
    except Exception as e:
        # Catch any other unexpected errors
        return {"ip": None, "error": f"An unexpected error occurred: {str(e)}"}


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

    # if validation fails, still try to get the Whois data
    if not validation_result["is_valid"]:
        return {
            "results for": domain_name,
            "error": validation_result["error"],
            "domain_registrar": get_domain_registrar_info(domain_name),
            "hosting_provider": None
        }

    domain_registrar = get_domain_registrar_info(domain_name)
    hosting_provider_ip = get_ipinfo(domain_name)
    hosting_provider = {}

    # handle errors in the IP lookup
    if hosting_provider_ip.get("error"):
        hosting_provider = {
            "ip": None,
            "lookup_url": None,
            "error": hosting_provider_ip["error"]
        }
    else:
        # if successful, generate the IPinfo lookup URL
        ipinfo_url = generate_ipinfo_link(hosting_provider_ip["ip"])
        hosting_provider = {
            "ip": hosting_provider_ip["ip"],
            "lookup_url": ipinfo_url,
            "error": None
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
# www.online-apd.com - dns does not resolve but has whois

# print(get_ipinfo("example.com"))  # Valid domain
# print(get_ipinfo("invalid-domain"))  # Invalid domain
# print(get_ipinfo(""))  # Empty input

# print(get_info('www.joesloandesign.com'))

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

