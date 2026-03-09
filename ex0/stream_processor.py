# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
# stream_processor.py                                :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
# By: asulon <asulon@student.42nice.fr>          +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
# Created: 2026/03/09 20:12:48 by asulon            #+#    #+#              #
# Updated: 2026/03/09 20:12:49 by asulon           ###   ########.fr        #
#                                                                           #
# ************************************************************************ #

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        pass


class NumericProcessor(DataProcessor):
    def validate(self, data) -> bool:
        return isinstance(data, int)

    def process(self, data):
        return super().process(data)


class TextProcessor(DataProcessor):
    def validate(self, data) -> bool:
        return isinstance(data, str)

    def process(self, data):
        return super().process(data)

# class LogProcessor(DataProcessor):
#     pass


def main():
    num = NumericProcessor()
    text = TextProcessor()
    for x in (num, text):
        print(x.validate(1))


if __name__ == "__main__":
    main()
