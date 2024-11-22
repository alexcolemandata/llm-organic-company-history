"""Generate and print data for a few silly industries"""
import argparse
from os import get_terminal_size
from .basis import make_data_for_industry, GeneratedData

HLINE = "-" * get_terminal_size().columns


def demo(industry: str) -> GeneratedData:
    print(f"\n{HLINE}\nGenerating data for {industry.title()}:\n")
    return make_data_for_industry(industry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate and print data for a specified industry."
    )
    parser.add_argument(
        "industry",
        type=str,
        help="The name of the industry for which to generate data.",
    )
    args = parser.parse_args()

    demo(args.industry)
