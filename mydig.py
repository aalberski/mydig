# Name: Adam Alberski
# Student ID: 112890087
# Date: 2/18/2022

import dns.resolver
import time
from datetime import datetime

# List of root servers
root = ['198.41.0.4','199.9.14.201','192.33.4.12','199.7.91.13','192.203.230.10','192.5.5.241','192.112.36.4','198.97.190.53',
'192.36.148.17','192.58.128.30','193.0.14.129','199.7.83.42','202.12.27.33']

# User input
domain = input('mydig ')

# Date and time of the request
WHEN = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Creates an initial query for the domain
request = dns.message.make_query(domain, dns.rdatatype.A)

question_section = request.question
answer_section = []

# Function to send a message recursively through a root server and additional/authority servers to find an answer
def send_query(req, addr):
    try:
        result = dns.query.udp(req, str(addr), 1)
        if(len(result.answer)==0):
            if(len(result.additional)!=0):
                for x in result.additional:
                    if(dns.rdatatype.to_text(x[0].rdtype)=='A'):
                        result = send_query(req, str(x[0]))
                        if(len(result.answer)!=0):
                            return result
            elif(len(result.authority)!=0):
                answer_section.append(str(result.authority[0]).splitlines()[0])
                for x in result.authority:
                    new_req = dns.message.make_query(str(x[0]), dns.rdatatype.A)
                    for x in root:
                        result = send_query(new_req,x)
                        if(len(result.answer)!=0):
                            answer_section.append(result.answer[0])
                            return result
        elif(str(result.answer).split()[3] != 'A'):
            answer_section.append(result.answer[0])
            new_req = dns.message.make_query(str(result.answer[0][0]), dns.rdatatype.A)
            for x in root:
                result = send_query(new_req, x)
                if(len(result.answer)!=0):
                    answer_section.append(result.answer[0])
                    return result
        else:
            if(len(answer_section)==0):
                answer_section.append(result.answer[0])
            return result
    except dns.exception.Timeout:
        print('timeout')
    except:
        print('Error')

# Start counting how long to resolve query
start = time.perf_counter()

# Finding an answer to the query
for x in root:
    response = send_query(request, x)
    if(len(response.answer)!=0):
        break

# Finish counting how long to resolve query
end = time.perf_counter()

# Question section
print('\nQUESTION SECTION:')
print(question_section[0])

# Answer section
print('\nANSWER SECTION:')
for a in answer_section:
    print(a)


# How much time it took to resolve the query
queryTime = (end - start) * 1000

# Terminal output for query time and when the query was made 
print('\nQuery Time: ' + str(queryTime) + ' ms')
print('WHEN: ' + WHEN)