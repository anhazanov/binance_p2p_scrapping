from db import Database

db = Database()
req = """DROP TABLE arbitrage;

CREATE TABLE arbitrage (
    id            INTEGER        PRIMARY KEY,
    profit        DECIMAL (4, 2),
    exchange1     VARCHAR (50)   NOT NULL,
    exchange2     VARCHAR (50)   NOT NULL,
    bank1         VARCHAR (50)   NOT NULL,
    bank2         VARCHAR (50)   NOT NULL,
    crypto_path   VARCHAR (50)   NOT NULL,
    role          VARCHAR (50)   NOT NULL,
    start_min     DECIMAL (6, 2) NOT NULL,
    start_max     DECIMAL (6, 2) NOT NULL,
    rates_path    VARCHAR (50)   NOT NULL,
    value         VARCHAR (5),
    exchange_path VARCHAR (1500) NOT NULL
);"""

db.creat(req)