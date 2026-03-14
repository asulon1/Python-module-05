# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  stream_processor.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42nice.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/03/13 15:49:17 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        """Process input data and return a result string."""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate input data for this processor."""

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    def validate(self, data: List[int]) -> bool:
        if not isinstance(data, List) or len(data) == 0:
            raise TypeError("Invalid list: list is empty or not a list")
        for d in data:
            if not isinstance(d, int):
                raise ValueError(
                    f"Invalid literal for int(): {d}")
        return True

    def process(self, data: List[int]) -> str:
        return f"Processing data: {data}"

    def format_output(self, result):
        total = 0
        for data in result:
            total += data
            average = total / len(result)
        return super().format_output((f"Processed {len(result)}"
                                      "numeric value,"
                                      f" sum={total}, "
                                      f"avg={average:.1f}"))


class TextProcessor(DataProcessor):
    def validate(self, data: str) -> bool:
        if not isinstance(data, str):
            raise TypeError(
                f"Expected a string for text processing, "
                f"but received {type(data).__name__} instead.")
        return True

    def process(self, data: str) -> str:
        return f'Processing data: "{data}"'

    def format_output(self, result: str) -> str:
        words = result.split()
        return super().format_output(("Processed text: "
                                      f"{len(result)} characters, "
                                      f"{len(words)} words"))


class LogProcessor(DataProcessor):
    def validate(self, data: str) -> bool:
        if not isinstance(data, str):
            raise TypeError(
                f"Expected a string for text processing, "
                f"but received {type(data).__name__} instead.")
        return True

    def process(self, data: str) -> str:
        return f'Processing data: "{data}"'

    def format_output(self, result: str) -> str:
        if "ERROR" in result:
            status = "[ALERT]"
        elif "INFO" in result:
            status = "[INFO]"
        return super().format_output((f"{status} {result.split(":")[0]} "
                                      "level detected:"
                                      f"{result.split(":")[1]}"))


def main():
    num = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    try:
        print("Initializing Numeric Processor...")
        num_data = [1, 2, 3, 4, 5]
        print(num.process(num_data))
        if num.validate(num_data) is True:
            print("Validation: Numeric data verified")
        else:
            print("Validation: Numeric data not verified")
        print(f"{num.format_output(num_data)}\n")
    except (TypeError, ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Text Processor...")
        text_data = "Hello Nexus World"
        print(text.process(text_data))
        if text.validate(text_data) is True:
            print("Validation: Text data verified")
        else:
            print("Validation: Text data not verified")
        print(f"{text.format_output(text_data)}\n")
    except (TypeError) as e:
        print(f"Error: {e}")

    try:
        print("Initializing Text Processor...")
        log_data = "ERROR: Connection timeout"
        # log_data = "INFO: System ready"
        print(log.process(log_data))
        if log.validate(log_data) is True:
            print("Validation: Log entry verified")
        else:
            print("Validation: Log entry not verified")
        print(log.format_output(log_data))
    except (ValueError, TypeError)as e:
        print(f"Error: {e}")

    print("\n=== Polymorphic Processing Demo ===")
    index = 1
    x = NumericProcessor()
    print(f"Result {index}: {x.process([1, 4, 7])}")

    index += 1
    x = TextProcessor()
    print(f"Result {index}: {x.validate("Hello world")}")
    index += 1
    x = LogProcessor()
    print(f"Result {index}: {x.format_output("INFO: System ready")}")


if __name__ == "__main__":
    main()
