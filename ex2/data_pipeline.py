# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_pipeline.py                                  :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/04/19 17:04:02 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List, Protocol, Union
from abc import ABC, abstractmethod


class DataProcessor(ABC):

    def __init__(self) -> None:
        self._data: List[str] = []
        self._output_index = 0

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
        index = self._output_index
        self._output_index += 1
        return (index, value)


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
        return False

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
                    f"{x.get('log_level', '')}: {x.get('log_message', '')}"
                )
        else:
            self._data.append(
                f"{data.get('log_level', '')}: {data.get('log_message', '')}"
            )


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        """Export processed data."""


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return

        csv_values = [value for _, value in data]
        print("CSV Output:")
        print(",".join(csv_values))


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        if not data:
            return

        items = []
        for index, value in data:
            items.append(f'"item_{index}": "{value}"')

        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self._streams:
            output_data: list[tuple[int, str]] = []

            for _ in range(nb):
                try:
                    output_data.append(proc.output())
                except Exception:
                    break

            if output_data:
                plugin.process_output(output_data)


def main():
    print("=== Code Nexus - Data Pipeline ===\n")

    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    data_proc = DataStream()
    data_proc.print_processors_stats()

    print("\nRegistering Processors")
    num = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    data_proc.register_processor(num)
    data_proc.register_processor(text)
    data_proc.register_processor(log)

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
    print("== DataStream statistics ==")
    data_proc.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    data_proc.output_pipeline(3, CSVExportPlugin())
    print("== DataStream statistics ==")
    data_proc.print_processors_stats()

    data = [
        21,
        ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
        [
            {
                'log_level': 'ERROR',
                'log_message': '500 server crash',
            },
            {
                'log_level': 'NOTICE',
                'log_message': 'Certificate expires in 10 days',
            },
        ],
        [32, 42, 64, 84, 128, 168],
        'World hello',
    ]

    print(f"Send another batch of data: {data}")
    data_proc.process_stream(data)
    print("== DataStream statistics ==")
    data_proc.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    data_proc.output_pipeline(5, JSONExportPlugin())
    print("== DataStream statistics ==")
    data_proc.print_processors_stats()


if __name__ == "__main__":
    main()
