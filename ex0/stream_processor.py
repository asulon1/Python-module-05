# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  stream_processor.py                               :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: asulon <asulon@student.42.fr>             +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 0026/03/09 20:12:48 by sulon           #+#    #+#               #
#  Updated: 2026/04/16 14:35:42 by asulon          ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from typing import Any, List, Union
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def ingest(self, data: Any) -> str:
        """Process input data"""

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate input data for this processor."""

    def output(self) -> tuple[int, str]:
        """Output ingest data"""


class NumericProcessor(DataProcessor):
    def validate(self, data: float | int | List[Union[int, float]]) -> bool:
        valid = False
        if isinstance(data, int):
            valid = True
        elif isinstance(data, float):
            valid = True
        elif all(isinstance(x, (int, float)) for x in data) and data:
            valid = True
        self.valid = valid
        return valid

    def ingest(self, data: float | int | List[Union[int, float]]) -> str:
        """Converts the data into strings and stores it internally"""
        if self.valid:
            self.data = str(data)
        return str(data)

    def output(self, result):
        total = 0
        for data in result:
            total += data
            average = total / len(result)
        return super().output((f"Processed {len(result)}"
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

    def ingest(self, data: str) -> str:
        return f'Processing data: "{data}"'

    def output(self, result: str) -> str:
        words = result.split()
        return super().output(("Processed text: "
                               f"{len(result)} characters, "
                               f"{len(words)} words"))


class LogProcessor(DataProcessor):
    def validate(self, data: str) -> bool:
        if not isinstance(data, str):
            raise TypeError(
                f"Expected a string for text processing, "
                f"but received {type(data).__name__} instead.")
        return True

    def ingest(self, data: str) -> str:
        return f'Processing data: "{data}"'

    def output(self, result: str) -> str:
        if "ERROR" in result:
            status = "[ALERT]"
        elif "INFO" in result:
            status = "[INFO]"
        return super().output((f"{status} {result.split(':')[0]} "
                               "level detected:"
                               f"{result.split(':')[1]}"))


def main():
    num = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()
    print("=== Code Nexus - Data Processor ===\n")
    try:
        print("Testing Numeric Processor...")
        number = 42
        num_float = 3.14
        int_list = [1, 2, 3, 4, 5]
        float_list = [1.1, 2.2, 3.3, 4.4, 5.5]
        invalid = "d"
        print(f"Trying to validate input '{number}': {num.validate(number)}")
        print(
            f"Trying to validate input '{num_float}': {num.validate(num_float)}")
        print(
            f"Trying to validate input '{int_list}': {num.validate(int_list)}")
        print(
            f"Trying to validate input '{float_list}': {num.validate(float_list)}")
        print(f"Trying to validate input '{invalid}': {num.validate(invalid)}")

        # print(num.ingest(num_data))
        # if num.validate(num_data) is True:
        #     print("Validation: Numeric data verified")
        # else:
        #     print("Validation: Numeric data not verified")
        # print(f"{num.output(num_data)}\n")
    except (TypeError, ValueError, ZeroDivisionError) as e:
        print(f"Error: {e}")

    # try:
    #     print("Initializing Text Processor...")
    #     text_data = "Hello Nexus World"
    #     print(text.ingest(text_data))
    #     if text.validate(text_data) is True:
    #         print("Validation: Text data verified")
    #     else:
    #         print("Validation: Text data not verified")
    #     print(f"{text.output(text_data)}\n")
    # except (TypeError) as e:
    #     print(f"Error: {e}")

    # try:
    #     print("Initializing Text Processor...")
    #     log_data = "ERROR: Connection timeout"
    #     # log_data = "INFO: System ready"
    #     print(log.ingest(log_data))
    #     if log.validate(log_data) is True:
    #         print("Validation: Log entry verified")
    #     else:
    #         print("Validation: Log entry not verified")
    #     print(log.output(log_data))
    # except (ValueError, TypeError)as e:
    #     print(f"Error: {e}")

    # print("\n=== Polymorphic Processing Demo ===")
    # index = 1
    # x = NumericProcessor()
    # print(f"Result {index}: {x.ingest([1, 4, 7])}")

    # index += 1
    # x = TextProcessor()
    # print(f"Result {index}: {x.validate('Hello world')}")
    # index += 1
    # x = LogProcessor()
    # print(f"Result {index}: {x.output('INFO: System ready')}")


if __name__ == "__main__":
    main()
