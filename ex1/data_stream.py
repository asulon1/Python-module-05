# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/04/19 16:49:02 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List, Union
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._data: List[str] = []

    @abstractmethod
    def ingest(self, data: Any) -> None:
        """Process input data"""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate input data for this processor."""

    def output(self) -> tuple[int, str]:
        """Output ingest data"""
        if not self._data:
            raise Exception("No data available")
        value = self._data.pop(0)
        return (0, value)


class NumericProcessor(DataProcessor):
    def validate(self, data: float | int | List[Union[int, float]]) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list):
            return all(isinstance(x, (int, float)) for x in data)
        return False

    def ingest(self, data: float | int | List[Union[int, float]]) -> None:
        if not self.validate(data):
            raise Exception("Got exception: Improper numeric data")

        if isinstance(data, list):
            for x in data:
                self._data.append(str(x))
        else:
            self._data.append(str(data))


class TextProcessor(DataProcessor):
    def validate(self, data: str | List[str]) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return all(isinstance(x, str) for x in data)

    def ingest(self, data: str | List[str]) -> None:
        if not self.validate(data):
            raise Exception("Got exception: Improper string data")

        if isinstance(data, list):
            for x in data:
                self._data.append(x)
        else:
            self._data.append(data)


class LogProcessor(DataProcessor):
    def validate(self, data: dict[str, str] | List[dict[str, str]]) -> bool:
        """Check type of dict[str, str] or List[dict[str, str]]"""
        # Check dict[str, str]
        if isinstance(data, dict) and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in data.items()
        ):
            return True

        # Check List[dict[str, str]]
        elif isinstance(data, list):
            return all(
                isinstance(di, dict) and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in di.items())
                for di in data
            )
        return False

    def ingest(self, data: dict[str, str] | List[dict[str, str]]) -> None:
        if not self.validate(data):
            raise Exception("Got exception: Improper log data")

        if isinstance(data, list):
            for x in data:
                self._data.append(
                    f"{x.get("log_level", '')}: {x.get("log_message", "")}")
        else:
            self._data.append(
                f"{data.get("log_level", '')}: {data.get("log_message", "")}")


class DataStream:
    def __init__(self) -> None:
        self._streams: List[DataProcessor] = []
        self._stats: dict[str, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self._streams.append(proc)
        self._stats[type(proc).__name__] = 0

    def process_stream(self, stream: List[Any]) -> None:
        for element in stream:
            handled = False

            for proc in self._streams:
                if proc.validate(element):
                    proc.ingest(element)

                    if isinstance(element, list):
                        self._stats[type(proc).__name__] += len(element)
                    else:
                        self._stats[type(proc).__name__] += 1

                    handled = True
                    break

            if not handled:
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {element}")

    def print_processors_stats(self) -> None:
        if not self._streams:
            print("No processor found, no data")
            return

        for proc in self._streams:
            name = type(proc).__name__
            total = self._stats[name]
            remaining = len(proc._data)

            print(f"{name.replace('Processor', ' Processor')}: total {total} "
                  f"items processed, remaining {remaining} on processor"
                  )


def main():
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    data_proc = DataStream()
    data_proc.print_processors_stats()

    print("\nRegistering Numeric Processor")
    num = NumericProcessor()
    data_proc.register_processor(num)
    data = [
        'Hello world',
        [3.14, -1, 2.71],
        [
            {
                'log_level': 'WARNING',
                'log_message': 'Telnet access! Use ssh instead',
            },
            {
                'log_level': 'INFO',
                'log_message': 'User wil is connected',
            },
        ],
        42,
        ['Hi', 'five'],
    ]
    print(f"Send first batch of data on stream: {data}")
    data_proc.process_stream(data)
    data_proc.print_processors_stats()

    print("\nRegistering other data processors")
    string = TextProcessor()
    log = LogProcessor()
    data_proc.register_processor(string)
    data_proc.register_processor(log)
    print("Send the same batch of data again")
    data_proc.process_stream(data)
    print("== DataStream statistics ==")

    data_proc.print_processors_stats()

    print("\nConsume some elements from the data processor: "
          "Numeric 3, Text 2, Log 1")
    for i in range(3):
        num.output()
    for i in range(2):
        string.output()
    for i in range(1):
        log.output()

    print("== DataStream statistics ==")
    data_proc.print_processors_stats()


if __name__ == "__main__":
    main()
