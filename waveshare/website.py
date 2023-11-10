
def Website():
    with open('home.html', 'r') as file:
        website = file.read()
    return website
