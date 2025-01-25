import whois
import socket

#using whois for now, will want to move to using rdap in the future

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
    # whois lookup
    domain_registrar = whois.whois(domain_name)
    # need to parse results for emails in the case no abuse email is listed
    # abuse_emails = []
    # emails = domain_registrar.get("emails", [])
    # if isinstance(emails, str):  # Handle single email case
    #     emails = [emails]
    # abuse_emails = [email for email in emails if "abuse" in email]
    return domain_registrar

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

# results = get_info("www.lukeandlouise.com")
# results = get_info("yieldscredit.com")
results = get_info("tabulation.co")
print(results[1])
