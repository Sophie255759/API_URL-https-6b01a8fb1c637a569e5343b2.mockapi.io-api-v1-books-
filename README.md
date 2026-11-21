import requests

API_URL = "https://6b01a8fb1c637a569e5343b2.mockapi.io/api/v1/books"
TIMEOUT = 10

def get_books():
    """GET all books."""
    try:
        response = requests.get(API_URL, timeout=TIMEOUT)
        response.raise_for_status()
        books = response.json()
        print("GET all books")
        print(books)
        print("Status code:", response.status_code)
        return books
    except requests.exceptions.RequestException as err:
        print("GET error:", err)
        return None

def add_book(book):
    """POST a new book."""
    try:
        response = requests.post(API_URL, json=book, timeout=TIMEOUT)
        response.raise_for_status()
        created_book = response.json()
        print("POST new book")
        print(created_book)
        print("Status code:", response.status_code)
        return created_book
    except requests.exceptions.RequestException as err:
        print("POST error:", err)
        return None

def update_book(book_id, book):
    """PUT: replace an existing book entirely."""
    try:
        response = requests.put(
            f"{API_URL}/{book_id}", json=book, timeout=TIMEOUT
        )
        response.raise_for_status()
        updated_book = response.json()
        print(f"PUT book {book_id}")
        print(updated_book)
        print("Status code:", response.status_code)
        return updated_book
    except requests.exceptions.RequestException as err:
        print("PUT error:", err)
        return None

def delete_book(book_id):
    """DELETE a book, then GET it to confirm it is gone."""
    try:
        response = requests.delete(f"{API_URL}/{book_id}", timeout=TIMEOUT)
        response.raise_for_status()
        print(f"DELETE book {book_id}")
        print("Status code:", response.status_code)
    except requests.exceptions.RequestException as err:
        print("DELETE error:", err)
        return

    try:
        check = requests.get(f"{API_URL}/{book_id}", timeout=TIMEOUT)
        if check.status_code == 404:
            print(f"Confirmed: book {book_id} no longer exists.")
        else:
            check.raise_for_status()
            print("Unexpected: book still exists!", check.json())
    except requests.exceptions.RequestException as err:
        print("Verification error:", err)

if __name__ == "__main__":
    get_books()

    add_book({
        "title": "Deep Work",
        "author": "Cal Newport",
        "rating": 8,
    })

    update_book(2, {
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "rating": 9,
    })

    delete_book(3)
