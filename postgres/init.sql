ALTER DATABASE postgres SET timezone TO 'Mexico/BajaNorte';

CREATE TABLE pings(
   id    SERIAL PRIMARY KEY           ,
   ip_id                INT   NOT NULL,
   date_time      TIMESTAMP   NOT NULL,
   time_ms     DECIMAL(8,3)   NOT NULL
);

CREATE TABLE ips(
   id    SERIAL PRIMARY KEY           ,
   ip                  TEXT   NOT NULL
);

ALTER TABLE pings ALTER COLUMN date_time SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE pings ADD FOREIGN KEY (ip_id) REFERENCES ips(id);
