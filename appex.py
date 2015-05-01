
import argparse

from sqlalchemy import Column, String, Table, and_, create_engine, func
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

def main():
    opts = parse_args()
    uri = "postgresql://{x.username}@{x.server}/{x.database}".format(x=opts)
    engine = create_engine(uri)
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
