# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/03/15 16:45:23 by asulon          ###   ########.fr        #
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

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if not criteria:
            return data_batch
        return [item for item in data_batch if criteria in str(item)]

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Retourne les statistiques de base du flux."""
        return {
            "id": self.stream_id,
            "type": self.type,
            "processed": self.batch_analysed
        }


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Environmental Data")
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
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
            except ValueError:
                raise ValueError(
                    f"need int of float, invalid: {split_data[1]}")
        return (
            f"Sensor analysis: {len(data_batch)} reading processed, "
            f"avg temp: {(total_temp / count_temp):2}°C\n ")

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "high_priority":
            # On considère critique si la valeur (après le :) est > 30
            critical_alerts = []
            for item in data_batch:
                try:
                    val = float(item.split(":")[1])
                    if val > 30:  # Logique arbitraire pour l'exemple
                        critical_alerts.append(item)
                except (ValueError, IndexError):
                    continue
            return critical_alerts
        return super().filter_data(data_batch, criteria)


class TransactionStream(DataStream):

    def __init__(self, stream_id: str):
        super().__init__(stream_id, "Financial Data")
        self.stream_id = stream_id
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
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
        return (
            f"Transaction analysis: {len(data_batch)} operations, "
            f"net flow: {total_amount:+} units\n ")

    def filter_data(
        self,
        data_batch: List[Any],
        criteria: Optional[str] = None
    ) -> List[Any]:
        if criteria == "high_priority":
            # On considère "large" si le montant est > 100
            return [
                item for item in data_batch
                if int(item.split(":")[1]) >= 100
            ]
        return super().filter_data(data_batch, criteria)


class EventStream(DataStream):

    def __init__(self, stream_id: str):
        super().__init__(stream_id, "System Events")
        self.stream_id = stream_id
        print(f"Stream ID: {self.stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:
        values = []
        total_error = 0
        for data in data_batch:
            if not isinstance(data, str):
                raise ValueError(f"str needed, invalid : f{data}")
            values.append(data)
            if data == "error":
                total_error += 1

        return (
            f"Event analysis: {len(data_batch)} events, "
            f"{total_error} error detected\n ")


class StreamProcessor:
    def __init__(self):
        self.streams: List[DataStream] = []
        self.batch_analysed = 0

    def add_stream(self, stream: DataStream):
        if isinstance(stream, DataStream):
            self.streams.append(stream)

    def process_all(self, data_batch: List[Any]) -> str:
        print("Processing mixed stream types through unified interface...\n")
        print("Batch 1 Results:")
        for stream in self.streams:
            batch = data_batch.get(stream.stream_id, [])
            res = stream.process_batch(batch)
            print(f"- {res.split(',')[0]}")

    def run_high_priority_filter(self, mixed_data: Dict[str, List[Any]]):
        print("Stream filtering active: High-priority data only")

        # On récupère les résultats filtrés
        sensor_stream = self.streams[0]  # Juste pour l'exemple
        trans_stream = self.streams[1]

        sensor_results = sensor_stream.filter_data(
            mixed_data[sensor_stream.stream_id], "high_priority")
        trans_results = trans_stream.filter_data(
            mixed_data[trans_stream.stream_id], "high_priority")

        print(
            f"Filtered results: {len(sensor_results)} critical sensor alerts, "
            f"{len(trans_results)} large transaction"
        )


def main():
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    sensor_data = ["temp:22.5", "humidity:65", "pressure:1013"]
    transaction_data = ["buy:100", "sell:150", "buy:75"]
    event_data = ["login", "error", "logout"]
    try:
        print("Initializing Sensor Stream...")
        sensor = SensorStream("SENSOR_001")
        print(f"Processing event batch: [{', '.join(sensor_data)}]")

        print(
            f"{sensor.process_batch(sensor_data)}")
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Transaction Stream...")
        transaction = TransactionStream("TRANS_001")

        print(f"Processing event batch: [{', '.join(transaction_data)}]")
        print(
            f"{transaction.process_batch(['buy:100', 'sell:150', 'buy:75'])}")
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Transaction Stream...")
        event = EventStream("EVENT_001")
        print(f"Processing event batch: [{', '.join(event_data)}]")
        print(f"{event.process_batch(['login', 'error', 'logout'])}")
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")

    print("=== Polymorphic Stream Processing ===")
    try:
        processor = StreamProcessor()
        processor.add_stream(sensor)
        processor.add_stream(transaction)
        processor.add_stream(event)

        mixed_data = {
            "SENSOR_001": ["temp:22.5", "humidity:65", "pressure:1013"],
            "TRANS_001": ["buy:1150", "sell:20", "buy:30", "buy:10"],
            "EVENT_001": ["login", "click", "logout"]
        }

        processor.process_all(mixed_data)

        print("\nStream filtering active: High-priority data only")
        crit_sensors = sensor.filter_data(
            mixed_data["SENSOR_001"], "high_priority")
        large_trans = transaction.filter_data(
            mixed_data["TRANS_001"], "high_priority")

        print(
            f"Filtered results: {len(crit_sensors)} critical sensor alerts, "
            f"{len(large_trans)} large transaction\n"
        )
        print("All streams processed successfully. Nexus throughput optimal.")

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
