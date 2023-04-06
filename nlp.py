#!/usr/bin/env python3
"""
Natuarl Language Password Generator.

Database source:
https://github.com/NaturalLanguagePasswords/system
"""
import argparse
import logging
import os
import sqlite3


class NaturalLanguagePassword(object):

    def __init__(self, database, self_random=False):
        self.log = logging.getLogger("nlp_gen")
        self.log.addHandler(logging.NullHandler())
        self._random = self_random
        self.db = sqlite3.connect(database)
        if not os.path.exists(database):
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
        cmd = " ".join([
               "SELECT `word` FROM `wordlist`",
               "WHERE adjective IS 1",
               "ORDER BY random() LIMIT 1" if not self._random else ""])
        return [x[0] for x in self.db.execute(cmd).fetchall()]

    def get_noun(self, plural=False):
        cmd = " ".join([
               "SELECT `word` FROM `wordlist`",
               "WHERE noun IS 1",
               "" if plural else "AND plural is 0",
               "ORDER BY random() LIMIT 1" if not self._random else ""])
        return [x[0] for x in self.db.execute(cmd).fetchall()]

    def close(self):
        self.db.close()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--length",
                        help="The Number of Adjective & noun pairs wanted. (Default 3)",
                        type=int, default=3)
    parser.add_argument("-c", "--count",
                        help="The number of password wanted.",
                        type=int, default=1)
    log_out = parser.add_mutually_exclusive_group()
    log_out.add_argument("-d", "--debug", help="Enable Debugging output.",
                         default=False, action="store_true")
    log_out.add_argument("-q", "--quiet",
                         help="Enable Quiet mode. Only prints the password",
                         default=False, action="store_true")
    args = parser.parse_args()

    if not args.quiet:
        logging.basicConfig(
            level=logging.DEBUG if args.debug else logging.INFO
        )

    passw = []
    passwords = []
    indent = ""
    with NaturalLanguagePassword("nlp.db") as nlp:
        for c in range(args.count):
            for _ in range(args.length):
                passw.append(nlp.get_adj()[0])
                passw.append(nlp.get_noun()[0])
            passwords.append("{}".format(" ".join(passw)))
            passw.clear()

    if not args.quiet:
        print("Your Password(s) is:\n", end="", flush=True)
        indent = "   "
    for pws in passwords:
        print(f"{indent}{pws}", end='' if args.quiet is True else '\n')
