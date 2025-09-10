#! python3
# phoneAndEmail.py - Finds phone numbers and email addresses on the clipboard.


"""
Escope:
    This code will perform a phone number and email address extraction from a clipbord tranfer area.
    When you press crt+c on a text. 
    page for text: https://nostarch.com/contactus
Modules:
    Regex
    pyperclip - 
"""

import pyperclip, re

phoneRegex = re.compile(r'''(
                        (\d{2,3}|\(\d{2,3}\))?          # area code
                        (\s|-|\.)?                      # separator
                        (\d{3,5})                       # first 5 digits
                        (\s|-|\.)                       # separator
                        (\d{4})                         # last 4 digits
                        (\s*(ext|x|ext.)\s*(\d{2,5}))?  # extension
                        )''', re.VERBOSE)

emailRegex = re.compile(r'''(
                        [a-zA-Z0-9._%+-]+   # username
                        @                   # symbol
                        [a-zA-Z0-9.-]+      # domain name
                        (\.[a-zA-Z]{2,4})   # dot samethins with 2 to 4 characters
                        )''', re.VERBOSE)

# Find matches in clipboard text.
text = str(pyperclip.paste())

matches = []
for groups in phoneRegex.findall(text):
    phoneNum = '-'.join([groups[1], groups[3], groups[5]])
    if groups[8] != '':
        phoneNum += ' x' + groups[8]
    matches.append(phoneNum)

qndPhoneNumber = len(matches)

for groups in emailRegex.findall(text):
    matches.append(groups[0])

qndEmails = len(matches) - qndPhoneNumber

# Copy results to the clipboard.
if len(matches) > 0:
    pyperclip.copy('\n'.join(matches))
    print('Copied to clipboard:')
    print('\n'.join(matches))
    print('We found {} phone numbers, and {} emails in the clipboard.'.format(qndPhoneNumber, qndEmails))

else:
    print('No phone numbers or email addresses found.')



