import whois
import socket


#using whois for now, will want to move to using rdap in the future,
#with a whois fallback when tld does not support rdap

###TBD - Get DNS Records


def get_ipinfo(ip_address):
    hosting_provider_ip = socket.gethostbyname(ip_address)
    return hosting_provider_ip

def generate_ipinfo_link(ip_address):
    # Generate IPinfo link
    if ip_address:
        return f"https://ipinfo.io/{ip_address}"
    return "no info"

def get_domain_registrar_info(domain_name):
    # whois lookup, want abuse contact
    domain_registrar = whois.whois(domain_name)

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


def get_info(domain_name):
    domain_registrar = get_domain_registrar_info(domain_name)
    hosting_provider_ip = get_ipinfo(domain_name)
    ipinfo_url = generate_ipinfo_link(hosting_provider_ip)
    results = [domain_registrar, hosting_provider_ip, ipinfo_url]
    #dictionairy for later:
    # results = {
    #     "domain_registrar": domain_registrar,
    #     "hosting_provider_ip": hosting_provider_ip,
    #     "ipinfo_url": ipinfo_url
    # }
    return results

# get_domain_registrar_info('www.holidaypartyevents.com')

# results = get_info("www.lukeandlouise.com")
# results = get_info("yieldscredit.com")
# results = get_info("tabulation.co")
# print(results[1])

# domain_lookup = whois.whois('www.holidaypartyevents.com')
# name = domain_lookup.get("registrar", [])
# registrar_url = domain_lookup.get("registrar_url", [] )
# print(name, registrar_url)


# NOTES on abuse contact formats:
#emails": "abuse@dnspod.com
#sometimes no emails, fall back to registar url
