ALTER DATABASE postgres SET timezone TO 'Mexico/BajaNorte';

CREATE TABLE pings(
   id    SERIAL PRIMARY KEY           ,
   ip_id                INT   NOT NULL,
   date_time      TIMESTAMP   NOT NULL,
   time_ms     DECIMAL(8,3)   NOT NULL
);

CREATE TABLE propietarios(
   id      SERIAL PRIMARY KEY               ,
   propietario   VARCHAR(70) NOT NULL UNIQUE 
);

CREATE TABLE modelos(
   id    SERIAL PRIMARY KEY                 ,
   modelo        VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE estatus(
   id    SERIAL PRIMARY KEY                  ,
   estatus       VARCHAR(25)  NOT NULL UNIQUE
);

CREATE TABLE ips(
   id    SERIAL PRIMARY KEY                  ,
   ip                  TEXT   NOT NULL UNIQUE,
   mac          VARCHAR(20)                  ,
   estatus_id           INT                  ,
   descripcion         TEXT                  ,
   propietario_id       INT                  ,
   modelo_id            INT                  ,
   extension    VARCHAR(5)                   ,
   fecha_registro      DATE   NOT NULL       ,
   es_monitoreado   BOOLEAN   NOT NULL
);

ALTER TABLE pings ALTER COLUMN date_time SET DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE pings ADD FOREIGN KEY (ip_id) REFERENCES ips(id);

ALTER TABLE ips ALTER COLUMN fecha_registro SET DEFAULT CURRENT_DATE;
ALTER TABLE ips ALTER COLUMN es_monitoreado SET DEFAULT TRUE;
ALTER TABLE ips ADD FOREIGN KEY (estatus_id) REFERENCES estatus(id);
ALTER TABLE ips ADD FOREIGN KEY (propietario_id) REFERENCES propietarios(id);
ALTER TABLE ips ADD FOREIGN KEY (modelo_id) REFERENCES modelos(id);

INSERT INTO  estatus(id, estatus) VALUES (1, 'Sin monitorear');
INSERT INTO  estatus(id, estatus) VALUES (2, 'Servidor encendido');
INSERT INTO  estatus(id, estatus) VALUES (3, 'Servidor apagado');