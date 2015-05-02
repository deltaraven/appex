# Copyright (c) 2015, Joel Miller <joel@deltaraven.com>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import argparse

from sqlalchemy import Column, String, Table, and_, create_engine, func
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased, sessionmaker
from sqlalchemy.dialects import postgresql # referenced so py2app bundles it up

Base = declarative_base()
Session = sessionmaker()

Tables = Table("tables", Base.metadata,
    Column("table_name", String, nullable=False),
    Column("table_schema", String, nullable=False),
    Column("table_type", String, nullable=False),
    schema="information_schema",
)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("database", help="Connect ")
    parser.add_argument("-s", "--server", metavar="HOST:PORT",
        default="localhost:5432", help="Connect to PostgreSQL server running "
        "at <%(metavar)s> (default=%(default)s)")
    parser.add_argument("-u", "--username", metavar="USERNAME",
        default="postgres", help="Connect as %(metavar)s (default=%(default)s)")
    return parser.parse_args()

def mkuri(opts, passwd=""):
    pwdstr = ":{}".format(passwd) if passwd else ""
    return "postgresql://{x.username}{pwdstr}@{x.server}/{x.database}".format(
        x=opts, pwdstr=pwdstr)

def authed_engine(opts):
    uri = mkuri(opts)
    engine = create_engine(uri)
    try:
        with engine.connect():
            pass
    except OperationalError as exc:
        if exc.message == "(psycopg2.OperationalError) fe_sendauth: no password supplied\n":
            from getpass import getpass
            passwd = getpass("Enter password for {}: ".format(opts.username))
            uri = mkuri(opts, passwd)
            engine = create_engine(uri)
        else:
            raise
    return engine

def main():
    opts = parse_args()
    engine = authed_engine(opts)
    print(engine)
    Session.configure(bind=engine)

    #SELECT table_name
    #    FROM information_schema.tables
    #    WHERE table_type='BASE TABLE'
    #    AND table_schema='public'
    #    ORDER BY LOWER(table_name);

    session = Session()
    columns = Tables.c
    query = session.query(Tables).filter(and_(
        columns.table_type=='BASE TABLE',
        columns.table_schema=='public',
    )).order_by(func.lower(columns.table_name))
    print("{} tables:".format(opts.database))
    for table in query.all():
        print("    {}".format(table.table_name))

if __name__ == "__main__":
    main()
