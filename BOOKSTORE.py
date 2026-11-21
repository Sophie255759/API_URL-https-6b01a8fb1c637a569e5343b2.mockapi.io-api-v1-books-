"""Exercise the Bookstore MockAPI books resource."""

import json
import sys

import requests

API_URL = "https://6b01a8fb1c637a569e5343b2.mockapi.io/api/v1/books"
TIMEOUT = 10
UPDATE_BOOK_ID = "2"
DELETE_BOOK_ID = "3"


def get_books():
    """Return all books in the inventory."""
    response = requests.get(API_URL, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def add_book(book):
    """Create a book and return the created record."""
    response = requests.post(API_URL, json=book, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def update_book(book_id, book):
    """Replace a book and return the updated record."""
    response = requests.put(
        f"{API_URL}/{book_id}", json=book, timeout=TIMEOUT
    )
    response.raise_for_status()
    return response.json()


def delete_book(book_id):
    """Delete a book and return whether a follow-up GET confirms removal."""
    response = requests.delete(f"{API_URL}/{book_id}", timeout=TIMEOUT)
    response.raise_for_status()

    verification = requests.get(f"{API_URL}/{book_id}", timeout=TIMEOUT)
    if verification.status_code == 404:
        return True
    verification.raise_for_status()
    return False


def main():
    """Run the GET, POST, PUT, DELETE, and deletion-verification exercise."""
    try:
        print("GET all books:")
        print(json.dumps(get_books(), indent=2))

        print("\nPOST a sixth book:")
        created = add_book({
            "title": "Deep Work",
            "author": "Cal Newport",
            "rating": "8",
        })
        print(json.dumps(created, indent=2))

        print(f"\nPUT book {UPDATE_BOOK_ID}:")
        updated = update_book(UPDATE_BOOK_ID, {
            "title": "The Psychology of Money",
            "author": "Morgan Housel",
            "rating": "9",
        })
        print(json.dumps(updated, indent=2))

        print(f"\nDELETE book {DELETE_BOOK_ID}:")
        if delete_book(DELETE_BOOK_ID):
            print(f"GET verification: book {DELETE_BOOK_ID} returned 404.")
        else:
            print(f"GET verification failed: book {DELETE_BOOK_ID} still exists.")
            return 1
    except requests.exceptions.RequestException as error:
        print(f"Bookstore API request failed: {error}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
