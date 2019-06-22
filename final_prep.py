deliver = {
    "sender": "Charlie",
    "recipient": "Anika",
    "price": 16.99,
    "status": "In Transit",
    "stops": ["New York", "Denver", "San Fran"]

}

books = [
    {"id": 1, "title": "Book A", "color": "blue", "year": 1901},
    {"id": 2, "title": "Book B", "color": "red", "year": 1957},
    {"id": 3, "title": "Book C", "color": "blue", "year": 1988},
    {"id": 4, "title": "Book D", "color": "green", "year": 1923},
    {"id": 5, "title": "Book E", "color": "yellow", "year": 2017},
]

person = {
    "stops": ["New York", "Denver", "San Fran"]
}

for x in person['stops']:
    print(x)

books_list = []

for x in books:
    if x['year'] >= 1951:
        books_list.append(x)

print(len(books_list))
        
def calculate_area(length, width):
    return length * width

area = calculate_area(4, 2)
print(area)

breakpoint()