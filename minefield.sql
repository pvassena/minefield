/******************************************************************************
	Create Database
*******************************************************************************/

DROP DATABASE IF EXISTS `MineField`;
DROP USER IF EXISTS 'minefield'@'localhost';

CREATE DATABASE `MineField`;
CREATE USER 'minefield'@'localhost' IDENTIFIED BY 'password';

GRANT ALL ON MineField.* TO 'minefield'@'localhost';

USE `MineField`;

/******************************************************************************
	Create Tables
*******************************************************************************/
CREATE TABLE `mine`
(
	`id`	INT NOT NULL AUTO_INCREMENT,
	`x`			INT NOT NULL,
	`y`			INT NOT NULL,
	`chunk_id`	INT NOT NULL,
	CONSTRAINT `PK_Mine` PRIMARY KEY (`id`)
);

CREATE TABLE `chunk`
(
	`id`	INT NOT NULL AUTO_INCREMENT,
	`i`			INT NOT NULL,
	`j`			INT NOT NULL,
	`board_id`	INT NOT NULL,
	CONSTRAINT `PK_Chunk` PRIMARY KEY (`id`)
);

CREATE TABLE `board`
(
	`id`	INT NOT NULL AUTO_INCREMENT,
	`chunk_size`	INT NOT NULL,
	`chunk_mines`	INT NOT NULL,
	CONSTRAINT `PK_Board` PRIMARY KEY (`id`)
);

CREATE TABLE `action`
(
	`id`	INT NOT NULL AUTO_INCREMENT,
	`chunk_id`	INT NOT NULL,
	`x`			INT NOT NULL,
	`y`			INT NOT NULL,
	`action`	ENUM ('DIG','SWITCH_FLAG') NOT NULL,
	CONSTRAINT `PK_Action` PRIMARY KEY (`id`)
);

/******************************************************************************
	Create Foreign Keys
*******************************************************************************/
ALTER TABLE `mine`
	ADD CONSTRAINT `Mine_ChunkID`
	FOREIGN KEY (`chunk_id`) References `chunk`(`id`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
ALTER TABLE `chunk`
	ADD CONSTRAINT `Chunk_BoardID`
	FOREIGN KEY (`board_id`) References `board`(`id`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
ALTER TABLE `action`
	ADD CONSTRAINT `Action_ChunkID`
	FOREIGN KEY (`chunk_id`) References `chunk`(`id`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
/******************************************************************************
	Create Foreign Index
*******************************************************************************/
CREATE INDEX `IFK_Mine_ChunkID`  ON `mine` (`chunk_id`);
CREATE INDEX `IFK_Chunk_BoardID` ON `chunk`(`board_id`);
