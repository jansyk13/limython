create table training_data (
	id INT AUTO_INCREMENT,
	source VARCHAR(50),
	time_stamp VARCHAR(50),
	method VARCHAR(50),
  url VARCHAR(1000),
  protocol VARCHAR(50),
  status INT(32),
  payload_size INT(32),
  PRIMARY KEY (id)
);
create table test_data (
	id INT AUTO_INCREMENT,
	source VARCHAR(50),
	time_stamp VARCHAR(50),
	method VARCHAR(50),
  url VARCHAR(1000),
  protocol VARCHAR(50),
  status INT(32),
  payload_size INT(32),
  PRIMARY KEY (id)
);
