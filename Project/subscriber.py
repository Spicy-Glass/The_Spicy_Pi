from google.cloud import pubsub_v1
import time
import json
from google.auth import jwt
import Pi

class Subscriber:
    def __init__(self, project_id, subscriber, topic_name):
        service_account_info = json.load(open("key.json"))
        audience = "https://pubsub.googleapis.com/google.pubsub.v1.Subscriber"
        credentials = jwt.Credentials.from_service_account_info(
            service_account_info, audience=audience
        )

        self._subscriber_obj = pubsub_v1.SubscriberClient(credentials=credentials)
        self.project_id = project_id
        self.subscriber_name = subscriber
        self.topic_name = topic_name
        self.subscriber_path = self._subscriber_obj.subscription_path(project_id, self.subscriber_name)

    def callback(self, message):
        """
        This function will be called every time a new message is pulled from
        the queue.
        :param message: object containing information about the incoming
        message
        :return:
        """
        decoded_message = message.data.decode("utf-8")  # DO not remove this!!
        try:
            message_dict = json.loads(decoded_message)
            recipient = message.attributes['recipient']
            if recipient == self.subscriber_name:
                print("Message is meant for this subscriber!\n")
                Pi.states_dic = message_dict
                Pi.check = 1
        except Exception as e:
            print(f"{decoded_message} was not a string dictionary.")
            print(f"Exception: {e}")
        message.ack()

    def start_server(self):
        """
        This function will indefinitely pull messages from the queue sent to
        the previously selected subscriber.
        :return:
        """
        print(f"Listening for messages on {self.subscriber_name}")
        print("...")

        streaming_pull_future = self._subscriber_obj.subscribe(
            self.subscriber_path, callback=self.callback
        )

        try:
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            print("Exiting Gracefully")
        except:
            streaming_pull_future.cancel()
