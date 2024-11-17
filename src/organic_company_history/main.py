"""Generate and print data for a few silly industries"""
from os import get_terminal_size

from .basis import make_data_for_industry, GeneratedData

HLINE = "-" * get_terminal_size().columns


def demo(industry: str) -> GeneratedData:
    print(f"\n{HLINE}\nGenerating data for {industry.title()}:\n")
    return make_data_for_industry(industry)


knitting = demo("occult detective agency")
space_coffee = demo("interstellar coffee delivery")
knitting = demo("knitting")
