import re

names = [
    'Finn Bindeballe',
    'Geir Anders Berge',
    'HappyCodingRobot',
    'Ron Cromberge',
    'Sohil',
    'Charles',
    'Brian Daugette',
    'Veronica Supersonica',
    'Tony Gasparovic',
    'Patrick Germann',
    'm!sha'
]

# Find people with first and last name only

#regex1 = '^(?P<fn>\w+)\s+(?P<ln>\w+)$' # START (group named 'fn' words) space (group named 'ln' words) END

#for name in names:
#    result = re.search(customRegex, name)
#    if result:
#        print(name)
#        print(result.group('fn'))

# Search for string sequence starting with C

#regex2 = 'C\w*'

#for name in names:
#    result = re.search(regex2, name)
#    if result:
#        print(name)
#        print(result.span())
#        print(result.group())

# Search for only single names

#regex3 = '^[a-zA-Z!]+$' # START match a string that starts with lowercase, uppercase or ! END (will exclude names with spaces)

#for name in names:
#    result = re.search(regex3, name)
#    if result:
#        print(name)

# Search for blocks of lower case letters 

#regex4 = '[a-z]+'
#for name in names:
#    result = re.findall(regex4, name)
#    if result:
#        print(result)
    
#    iteratedResult = re.finditer(regex4, name)
#    for match in iteratedResult:
#        print(match)

# Search URLs, find strings that start with http or https

links = [
    'https://www.socratica.com',
    'http://www.socratica.org',
    'file://test.this.path.if.it.works.pdf',
    'com.socratica.www_https://'
]

regex5 = 'https?'
regex6 = 'https?://w{3}.\w+.(com|org)'
regex7 = '^file://(\w+.)+.pdf'

for link in links:
    if re.fullmatch(regex6, link):
        print(link)