import whois
import socket

#using whois for now, will want to move to using rdap in the future

###TBD - Get DNS Records


def get_info(domain_name):
    #whois lookup
    domain_registrar = whois.whois(domain_name)
    #need to parse results for emails in the case no abuse email is listed

    # abuse_emails = []
    # emails = domain_registrar.get("emails", [])
    # if isinstance(emails, str):  # Handle single email case
    #     emails = [emails]
    # abuse_emails = [email for email in emails if "abuse" in email]
    #
    # #hosting provider finder
    hosting_provider_ip = socket.gethostbyname(domain_name)
###TBD - ipinfo lookup
    # Generate IPinfo link
    ipinfo_url = f"https://ipinfo.io/{hosting_provider_ip}"
    results = [domain_registrar, hosting_provider_ip, ipinfo_url]
    return results

results = get_info("www.lukeandlouise.com")
# results = get_info("yieldscredit.com")
# results = get_info("tabulation.co")
print(results[2])
