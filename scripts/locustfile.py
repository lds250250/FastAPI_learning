from locust import HttpUser, between, task

USERNAME = "admin"
PASSWORD = "secret123"
ISBN = "9787115428028"


class LibraryUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self) -> None:
        response = self.client.post(
            "/token",
            data={"username": USERNAME, "password": PASSWORD},
        )
        token = response.json()["access_token"]
        self.client.headers["Authorization"] = f"Bearer {token}"

    @task(3)
    def list_books(self) -> None:
        self.client.get("/books/")

    @task(1)
    def get_one_book(self) -> None:
        self.client.get(f"/books/{ISBN}")
