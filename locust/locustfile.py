import time
import datetime
import uuid
from random import randrange
from locust import FastHttpUser, task, between

class QuickstartUser(FastHttpUser):
    wait_time = between(0.5, 2)

    @task
    def NavigateAllPagesToExperiment(self):
        self.client.get("/consent")
        self.client.get("/main")
        self.client.get("/experiment-survey")
        self.client.post("http://34.116.223.97:3000/surveys/scale", json={"userId": self.userId, "answers": [randrange(2), randrange(5), randrange(5), randrange(5)], "experimentNumber": randrange(7)})

    @task
    def StartExperiment(self):
        self.client.get("/consent")
        self.client.get("/main")

    @task
    def GoToConsent(self):
        self.client.get("/consent")

    def on_start(self):
        self.client.get("/")
        response = self.client.post("http://34.116.223.97:3000/users/connect", json={"connectedTime": datetime.datetime.now().timestamp()})
        if response.status_code == 201:
            try:
                self.userId = response.json()["userId"]
            except JSONDecodeError:
                response.failure("Response was not JSON")
            except KeyError:
                response.failure("userId not key in the response JSON")
        else
            response.failure("User was not created correctly")
        