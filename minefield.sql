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
CREATE TABLE `Mine`
(
	`MineID`	INT NOT NULL AUTO_INCREMENT,
	`ChunkID`	INT NOT NULL,
	`x`			TINYINT NOT NULL,
	`y`			TINYINT NOT NULL,
	CONSTRAINT `PK_Mine` PRIMARY KEY (`MineID`)
);

CREATE TABLE `Chunk`
(
	`ChunkID`	INT NOT NULL AUTO_INCREMENT,
	`BoardID`	INT NOT NULL,
	`i`			INT NOT NULL,
	`j`			INT NOT NULL,
	CONSTRAINT `PK_Chunk` PRIMARY KEY (`ChunkID`)
);

CREATE TABLE `Board`
(
	`BoardID`	INT NOT NULL AUTO_INCREMENT,
	`ChunkSize`	INT NOT NULL,
	`ChunkMines`	INT NOT NULL,
	CONSTRAINT `PK_Board` PRIMARY KEY (`BoardID`)
);

CREATE TABLE `Action`
(
	`ActionID`	INT NOT NULL AUTO_INCREMENT,
	`ChunkID`	INT NOT NULL,
	`x`			INT NOT NULL,
	`y`			INT NOT NULL,
	`Action`	ENUM ('Dig','SwitchFlag') NOT NULL,
	CONSTRAINT `PK_Action` PRIMARY KEY (`ActionID`)
);

/******************************************************************************
	Create Foreign Keys
*******************************************************************************/
ALTER TABLE `Mine`
	ADD CONSTRAINT `Mine_ChunkID`
	FOREIGN KEY (`ChunkID`) References `Chunk`(`ChunkID`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
ALTER TABLE `Chunk`
	ADD CONSTRAINT `Chunk_BoardID`
	FOREIGN KEY (`BoardID`) References `Board`(`BoardID`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
ALTER TABLE `Action`
	ADD CONSTRAINT `Action_ChunkID`
	FOREIGN KEY (`ChunkID`) References `Chunk`(`ChunkID`)
	ON UPDATE NO ACTION
	ON DELETE NO ACTION;
	
/******************************************************************************
	Create Foreign Index
*******************************************************************************/
CREATE INDEX `IFK_Mine_ChunkID`  ON `Mine` (`ChunkID`);
CREATE INDEX `IFK_Chunk_BoardID` ON `Chunk`(`BoardID`);
