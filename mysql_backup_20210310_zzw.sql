-- Dump created by MySQL pump utility, version: 8.0.23, Win64 (x86_64)
-- Dump start time: Wed Mar 10 15:49:34 2021
-- Server version: 8.0.23

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE;
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET @@SESSION.SQL_LOG_BIN= 0;
SET @OLD_TIME_ZONE=@@TIME_ZONE;
SET TIME_ZONE='+00:00';
SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT;
SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS;
SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION;
SET NAMES utf8mb4;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ `zzw` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
CREATE TABLE `zzw`.`ab` (
`a` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`aba` (
`id` int NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
INSERT INTO `zzw`.`ab` VALUES ("2019-05-30 14:23:36");
CREATE TABLE `zzw`.`abekey` (
`id` int NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`ccc` (
`id` int NOT NULL AUTO_INCREMENT,
`vl` varchar(56) NOT NULL,
PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`mer` (
`Id` int DEFAULT NULL,
`v` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
INSERT INTO `zzw`.`aba` VALUES (1),(2);
CREATE TABLE `zzw`.`rrrrrrrrrrrrr` (
`a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`sdg` (
`a` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
INSERT INTO `zzw`.`abekey` VALUES (1),(2),(3),(4),(50);
CREATE TABLE `zzw`.`t` (
`name` varchar(64) DEFAULT NULL,
`ts` datetime(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`t4` (
`a` int NOT NULL,
`uid` binary(16) DEFAULT (uuid_to_bin(uuid())),
PRIMARY KEY (`a`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`test` (
`a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
INSERT INTO `zzw`.`mer` VALUES (1,"qqqqq"),(2,"aaaaaa"),(3,"bbbbbb"),(4,"cccccc"),(5,"ddddddd"),(6,"457"),(7,"Ëµµ");
CREATE TABLE `zzw`.`test2` (
`name` varchar(36) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`test3` (
`name` char(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`test4` (
`a` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`test5` (
`a` binary(16) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
CREATE TABLE `zzw`.`ttttttttttttt` (
`a` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` FUNCTION `zzw`.`account_count3`() RETURNS int
    DETERMINISTIC
begin
       declare a int default 2147483647;
			 declare b int default 2147483647;
			 declare c int default 0;
       set c = a + b;
		   RETURN c;
end//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER="root"@"localhost" PROCEDURE `zzw`."abc"("@Id" int)
BEGIN
	select * From test where a="@Id";
	END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER="root"@"localhost" PROCEDURE `zzw`."abcd"("@Id" int)
BEGIN
	select * From test where a="@Id";
	END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`abekey`()
BEGIN	
	DECLARE EXIT HANDLER FOR SQLEXCEPTION,SQLWARNING
  BEGIN
   ROLLBACK;
	 RESIGNAL;
  END;

	
#START TRANSACTION;
set @a=1;
INSERT into abekey(id) VALUES(50);
INSERT into abekey(id) VALUES(4);

set @a=100;
set @b = 1;
#COMMIT;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`ac`()
begin
    declare aa bit;
    declare bb Boolean;
DECLARE a int;

  set aa=0;
  set bb=1;
  select aa,bb;
  
  
  SET a=4321;
  SELECT a FROM test t;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`account_count`()
BEGIN
       declare a int default 2147483647;
			 declare b int default 2147483647;
			 declare c int default 0;
     select a + b;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`account_count2`()
BEGIN
       declare a int default 2147483647;
			 declare b int default 2147483647;
			 declare c int default 0;
     set c = a + b;
		 SELECT c;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`asdbadsg`()
BEGIN
    ada: BEGIN
      
      DECLARE LastEnding DECIMAL(28,11);
      
      SELECT LastEnding = 1 FROM test t WHERE 1=1 LIMIT 1;
      SELECT LastEnding;
      
      SELECT 1;
      LEAVE ada;
      
      SELECT 2;
    END ada;
    
    SELECT 3;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`sd`(a int,b int,OUT c int)
BEGIN
     
  	DECLARE EXIT HANDLER FOR SQLEXCEPTION
  BEGIN
      set c=-9;
      ROLLBACK;
    RESIGNAL;
  END;
START TRANSACTION;

        SIGNAL SQLSTATE '45001'
      SET MESSAGE_TEXT = 'Ê≠§Ê≤ôÁõòÊï∞ÊçÆÊó†Ê≥ïÁâ©ÁêÜÂà†Èô§!';

  INSERT INTO aba(id) VALUES (1000);
  
  #SET c = 0;

  INSERT INTO aba(id) VALUES (1);

  INSERT INTO aba(id) VALUES (200);
     set c = a + b;
		 SELECT a + b;
  COMMIT;

  BEGIN
    DECLARE i int DEFAULT 0;
    END;
 END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`sd2`(a int,b int)
BEGIN
  DECLARE id int DEFAULT 0;
	SELECT @X,id;

  DELETE FROM aba c WHERE c.id=id;
 END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`se`()
begin
       select * From zzw.test;
			 select *,r From zzw.test5 t;
END//
DELIMITER ;
;
DELIMITER //
CREATE DEFINER=`root`@`localhost` PROCEDURE `zzw`.`sp1`(x VARCHAR(5))
BEGIN
  DECLARE xname VARCHAR(5) DEFAULT 'bob';
  DECLARE newname VARCHAR(5);
  DECLARE xid INT;

  SELECT x, 1 INTO newname, xid;
  SELECT newname,xid;
END//
DELIMITER ;
;
INSERT INTO `zzw`.`t4` VALUES (1,_binary "\…\'•π£ªÈõòê+4kç"),(2,_binary "\…/∫©£ªÈõòê+4kç"),(3,_binary "\…6!†£ªÈõòê+4kç");
USE `zzw`;
ALTER TABLE `zzw`.`mer` ADD UNIQUE KEY `Id` (`Id`);
INSERT INTO `zzw`.`test2` VALUES ("cad8d29a-7c66-11e9-bd74-902b341b6b8d"),("Ëµµ");
INSERT INTO `zzw`.`test3` VALUES ("Ëµµ"),("ËµµÂ≠ê");
INSERT INTO `zzw`.`test4` VALUES (1);
INSERT INTO `zzw`.`test5` VALUES (_binary "1\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"),(_binary "245347\0\0\0\0\0\0\0\0\0\0");
USE `zzw`;
ALTER TABLE `zzw`.`t4` ADD KEY `Index_t4_uid` (`uid`) USING BTREE;
USE `zzw`;
ALTER TABLE `zzw`.`test4` ADD UNIQUE KEY `a` (`a`);
SET TIME_ZONE=@OLD_TIME_ZONE;
SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT;
SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS;
SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
SET SQL_MODE=@OLD_SQL_MODE;
-- Dump end time: Wed Mar 10 15:49:34 2021
