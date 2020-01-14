from kafka import KafkaProducer
import json
import time


class ProducerServer(KafkaProducer):

    def __init__(self, input_file: str, topic: str, **kwargs):
        super().__init__(**kwargs)
        self.input_file = input_file
        self.topic = topic

    # TODO we're generating a dummy data
    def generate_data(self):
        with open(self.input_file) as f:
            json_data = json.load(f)
            for data in json_data:
                message = self.dict_to_binary(data)
                # TODO send the correct data
                self.send(
                    topic=self.topic,
                    value=message
                )
                time.sleep(1)

    # TODO fill this in to return the json dictionary to binary
    def dict_to_binary(self, json_dict: dict):
        return json.dumps(json_dict).encode('utf-8')
