# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_processor.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/04/18 16:57:01 by asulon          ###   ########.fr        #
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


def main():
    print("=== Code Nexus - Data Processor ===\n")

    """Numeric Processor"""
    print("Testing Numeric Processor...")
    num = NumericProcessor()
    print(f"Trying to validate input '42': {num.validate(42)}")
    print(f"Trying to validate input 'Hello': {num.validate('Hello')}")
    try:
        print("Test invalid ingestion of string 'foo' "
              "without prior validation:")
        num.ingest("foo")
    except Exception as error:
        print(error)
    print("Processing data: [1, 2, 3, 4, 5]")
    num.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for i in range(3):
        _, value = num.output()
        print(f"Numeric value {i}: {value}")

    """Text Processor"""
    print("\nTesting Text Processor...")
    text = TextProcessor()
    print(f"Trying to validate input '42': {text.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    print("Extracting 1 values...")
    text.ingest(['Hello', 'Nexus', 'World'])
    for i in range(1):
        _, value = text.output()
        print(f"Text value {i}: {value}")

    """Log Processor"""
    print("\nTesting Log Processor...")
    log = LogProcessor()
    print(f"Trying to validate input '42': {log.validate("Hello")}")

    log_dict = [{
        'log_level': 'NOTICE',
        'log_message': 'Connection to server'
    },
        {
        'log_level': 'ERROR',
        'log_message': 'Unauthorized access!!'
    }]
    print(
        f"Processing data {log_dict}")
    log.ingest(log_dict)
    for i in range(2):
        _, value = log.output()
        print(f"Log entry {i}: {value}")


if __name__ == "__main__":
    main()
