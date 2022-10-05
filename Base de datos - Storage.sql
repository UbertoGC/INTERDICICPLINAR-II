CREATE DATABASE Almacen;
USE  Almacen;

CREATE TABLE usuario(
	id_user INT PRIMARY KEY auto_increment,
	correo VARCHAR(45),
	password_ VARCHAR(45)
);

CREATE TABLE almacen(
	id_alm INT PRIMARY KEY auto_increment,
    id_user INT,
	nombre VARCHAR(45),
	descripcion TEXT,
	FOREIGN KEY (id_user) REFERENCES usuario (id_user)
);
CREATE TABLE items(
	id_item INT auto_increment,
    id_alm INT,
    cantidad INT,
    unidad varchar(50),
    nombre varchar(50),
	PRIMARY KEY (id_item),
    FOREIGN KEY (id_alm) REFERENCES almacen (id_alm)
);

SELECT * FROM usuario;
INSERT INTO usuario VALUES(1,'rutierrezar@unsa.edu.pe', 123456);
INSERT INTO usuario VALUES(2,'asd_34j3@unsa.edu.pe', '123fdsh3');
INSERT INTO usuario VALUES(3,'eef_aragr@unsa.edu.pe', '_eeeer56');

SELECT * FROM almacen;
INSERT INTO almacen VALUES(1,1,'Ropas','Ropasde todas las marcas y colores - H&M');
INSERT INTO almacen VALUES(2,1,'Frutas','Frutas del mercado San Camilo');

SELECT * FROM items;
INSERT INTO items VALUES(1,1,'camisa roja');
INSERT INTO items VALUES(2,1,'pantalon negro');
INSERT INTO items VALUES(3,1,'chalina negra');

INSERT INTO items VALUES(4,2,'4 kilos de papaya');
INSERT INTO items VALUES(5,2,'3 cajas de fresa');
INSERT INTO items VALUES(6,2,'4 cajas de uvas');

CALL crearUsuario('rutierrezar@unsa.edu.pe',123456);
