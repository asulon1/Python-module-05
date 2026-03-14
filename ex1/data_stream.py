# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/03/14 21:34:28 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataStream(ABC):
    def __init__(self, stream_id: str, type: str):
        self.stream_id = stream_id
        self.type = type
        self.batch_analysed = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Environmental Data")
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
        print(f"Processing sensor batch: [{', '.join(data_batch)}]")
        values = []
        total_temp = 0
        count_temp = 0
        for data in data_batch:
            split_data = data.split(":")
            try:
                values.append(float(split_data[1]))
                if split_data[0] == "temp":
                    total_temp += float(split_data[1])
                    count_temp += 1
                self.batch_analysed += 1
            except ValueError:
                raise ValueError(
                    f"need int of float, invalid: {split_data[1]}")
        print(
            f"Sensor analysis: {self.batch_analysed} reading processed, "
            f"avg temp: {total_temp / self.batch_analysed}°C\n ")


class TransactionStream(DataStream):

    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Financial Data")
        self.stream_id = stream_id
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
        print(f"Processing transaction batch: [{', '.join(data_batch)}]")
        values = []
        total_amount = 0
        for data in data_batch:
            split_data = data.split(":")
            try:
                values.append(int(split_data[1]))
                if split_data[0] == "buy":
                    total_amount += int(split_data[1])
                elif split_data[0] == "sell":
                    total_amount -= int(split_data[1])
                self.batch_analysed += 1
            except ValueError:
                raise ValueError(
                    f"need int of float, invalid: {split_data[1]}")
        print(
            f"Transaction analysis: {self.batch_analysed} operations, "
            f"net flow: {total_amount:+} units\n ")


class EventStream(DataStream):

    def __init__(self, stream_id: str):
        super().__init__(stream_id, "System Events")
        self.stream_id = stream_id
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
        print(f"Processing event batch: [{', '.join(data_batch)}]")
        values = []
        total_error = 0
        for data in data_batch:
            if not isinstance(data, str):
                raise ValueError(f"str needed, invalid : f{data}")
            values.append(data)
            if data == "error":
                total_error += 1

            self.batch_analysed += 1
        print(
            f"Event analysis: {self.batch_analysed} events, "
            f"{total_error} error detected\n ")


class StreamProcessor(DataStream):
    def __init__(self, dataList: List[Any]):
        # recoit une list de data et repartir sur les differentes classes ??
        pass


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    try:
        print("Initializing Sensor Stream...")
        sensor = SensorStream("SENSOR_001")
        sensor.process_batch(["temp:2.5", "humidity:65", "pressure:1013"])
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Transaction Stream...")
        transaction = TransactionStream("TRANS_001")
        transaction.process_batch(["buy:100", "sell:150", "buy:75"])
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Transaction Stream...")
        event = EventStream("EVENT_001")
        event.process_batch(["login", "error", "logout"])
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

        print("=== Polymorphic Stream Processing ===")
        print("All streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
