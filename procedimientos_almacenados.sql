DELIMITER //
drop procedure if exists `crearUsuario`;//
CREATE DEFINER=`root`@`localhost` PROCEDURE `crearUsuario`(IN n_email varchar(50),
IN n_contra varchar(30))
BEGIN
	IF(select exists (select 1 from usuario where correo = n_email)) then
		select 'Usuario ya existe!!';
	ELSE
		insert into usuario values (n_email, n_contra);
	END IF;
END;
//
DELIMITER ;