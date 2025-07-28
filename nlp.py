#!/usr/bin/env python3
"""
Natural Language Password Generator.

Database source:
https://github.com/NaturalLanguagePasswords/system
"""

import argparse
import itertools
import logging
import pathlib
import sqlite3

__version__ = "0.1.0"


class NaturalLanguagePassword:
    def __init__(self, database, self_random=True):
        self.log = logging.getLogger("nlp_gen")
        self.log.addHandler(logging.NullHandler())
        self._random = self_random
        self.db = sqlite3.connect(str(database))
        if not database.exists():
            self._create()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def _create(self):
        create_str = (
            "CREATE TABLE `wordlist` ( "
            "`word` text NOT NULL UNIQUE, "
            "`adjective` int DEFAULT 0, "
            "`noun` int DEFAULT 0, "
            "`plural` int DEFAULT 0, "
            "`nlp` int DEFAULT 0, "
            "PRIMARY KEY (`word`) );"
        )
        with self.db as database:
            database.execute(create_str)

    def add(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def count_adj(self):
        cmd = "SELECT COUNT(*) FROM `wordlist` WHERE adjective IS 1"
        return self.db.execute(cmd).fetchall()[0][0]

    def count_noun(self, plural=False):
        cmd = "SELECT COUNT(*) FROM `wordlist` WHERE noun IS 1"
        if not plural:
            cmd += "AND plural is 0"
        return self.db.execute(cmd).fetchall()[0][0]

    def get_adj(self):
        cmd = " ".join(
            [
                "SELECT `word` FROM `wordlist`",
                "WHERE adjective IS 1",
                "ORDER BY random() LIMIT 1" if self._random else "",
            ],
        )
        return self.db.execute(cmd).fetchone()[0]

    def get_noun(self, plural=False):
        cmd = " ".join(
            [
                "SELECT `word` FROM `wordlist`",
                "WHERE noun IS 1",
                "" if plural else "AND plural is 0",
                "ORDER BY random() LIMIT 1" if self._random else "",
            ],
        )
        return self.db.execute(cmd).fetchone()[0]

    def close(self) -> None:
        self.db.close()


def get_password(pair_len=3):
    """
    Get pair_len amount of Adjective & Noun pair back as string.

    Args:
        pair_len: The number of Adjective & Noun pairs.
    Returns:
        A string where the adjective & noun pairs are space separated.
    """
    db_file = pathlib.Path("nlp.db")
    with NaturalLanguagePassword(db_file) as nlp:
        return " ".join([
            f"{nlp.get_adj()} {nlp.get_noun()}"
            for _ in itertools.repeat(None, pair_len)
        ])


def main():
    logging_level_map = {
        1: 50,
        2: 40,
        3: 30,
        4: 20,
        5: 10,
    }

    parser = argparse.ArgumentParser(prog="nlp")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"v{__version__}",
    )
    parser.add_argument(
        "-l",
        "--length",
        help="The Number of Adjective & noun pairs wanted. (Default: 3)",
        type=int,
        default=3,
    )
    parser.add_argument(
        "-c",
        "--count",
        help="The number of password wanted. (Default: 1)",
        type=int,
        default=1,
    )
    log_out = parser.add_mutually_exclusive_group()
    log_out.add_argument(
        "--verbose",
        type=int,
        default=0,
        choices=range(6),
        metavar="[0-5]",
        help="Set the logging level. 0=Off, 1=Critical, 2=Error, 3=Warning, 4=Info, 5=Debug",
    )
    log_out.add_argument(
        "-s",
        "--silence",
        help="Enable script/silence mode. Only prints the password",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    if args.verbose:
        level = logging_level_map.get(args.verbose, logging.NOTSET)
        logging.basicConfig(level=level)

    indent = "" if args.silence else "   "
    p_end = "" if args.silence is True else "\n"

    if not args.silence:
        print("Your Password(s) is:\n", end="", flush=True)
    for _ in range(args.count):
        print(f"{indent}{get_password(args.length)}", end=p_end)

if __name__ == "__main__":
    main()
