"""
this is the main.py from which the program will run
"""

import retrieve
import news_info
import alcParse
import yahoo
import linked_in


def main():
    getter = retrieve.Retriever()
    events = getter.getEvents()
    


if __name__ == "__main__":
    main()
