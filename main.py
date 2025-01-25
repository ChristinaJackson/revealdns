import whois
import socket

# phase 1: rough testing
# res = whois.whois("inconcert.cl")
# res2 = whois.whois("https://tabulation.co/")
#
# print(res2.registrar_url)
# print(res.registrar_url)
# print(res2)
#
# value = socket.gethostbyname("inconcert.cl")
# print(value)
#

#moved into a very basic function
def get_info(domain_name):
    domain_registar = whois.whois(domain_name)
    hosting_provider_ip = socket.gethostbyname(domain_name)
    # print (domain_registar, hosting_provider)
    results = [domain_registar, hosting_provider]
    return results


results = get_info("www.lukeandlouise.com")
results = get_info("yieldscredit.com")
results = get_info("tabulation.co")
print(results[0])