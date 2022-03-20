CREATE TABLE IF NOT EXISTS pokemon (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(16) NOT NULL UNIQUE,
    `number` INT(4) unsigned NOT NULL UNIQUE,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    description VARCHAR(255) NOT NULL UNIQUE,
    base_xp SMALLINT(4) unsigned NOT NULL,
    sprite VARCHAR(255) NOT NULL UNIQUE,
    hp INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL,
    special_attack INT NOT NULL,
    special_defense INT NOT NULL,
    speed INT NOT NULL,
    male FLOAT,
    female FLOAT,
    shiny_male FLOAT,
    shiny_female FLOAT,
    PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS abilities (
    ID INT NOT NULL AUTO_INCREMENT,
    normal_ability VARCHAR(255),
    hidden_ability VARCHAR(255),
    PRIMARY KEY (ID)
);

CREATE TABLE types (
    ID INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (ID)
);

CREATE TABLE relAbilitiesPokemon (
    ID INT NOT NULL AUTO_INCREMENT,
    pokemonID INT NOT NULL,
    abilityID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (pokemonID) REFERENCES pokemon(ID),
    FOREIGN KEY (abilityID) REFERENCES abilities(ID)
);

CREATE TABLE relTypesPokemon (
    ID INT NOT NULL AUTO_INCREMENT,
    pokemonID INT NOT NULL,
    typeID INT NOT NULL,
    PRIMARY KEY (ID),
    FOREIGN KEY (pokemonID) REFERENCES pokemon(ID),
    FOREIGN KEY (typeID) REFERENCES types(ID)
);