\c flat_box;

CREATE TABLE apartments (
  id serial NOT NULL,
  lat numeric NOT NULL,
  lon numeric NOT NULL,
  rooms integer NOT NULL,
  area numeric NOT NULL,
  CONSTRAINT apartments_pk PRIMARY KEY (id)
);
