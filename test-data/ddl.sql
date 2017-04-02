create table data (
	id INT AUTO_INCREMENT,
	source VARCHAR(255),
	time_stamp VARCHAR(255),
	method VARCHAR(255),
  url VARCHAR(2048),
  protocol VARCHAR(255),
  status INT(32),
  payload_size INT(32),
  PRIMARY KEY (id)
);
