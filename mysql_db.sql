-- MYSQL VERSION --
--
--
-- Might want to add other data points (eg: email size) depending what the client actually wants from ther analytics

CREATE TABLE `emails` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `from_user_id` int(11) NOT NULL COMMENT 'id number for user in user table',
  `to_user_id` int(11) NOT NULL COMMENT 'id number for user in user table',
  `subject` varchar(200) NOT NULL DEFAULT 'No Subject',
  `datetime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- Not sure about threading. On one hand it would be useful to track ongoing exchanges, on the other not sure
-- how easy it is to get accurate data about this out of IMAP. Plus plenty of people just reply to the last
-- message to start a new conversation. Realistically speaking an exchange between mentor and mentee might get
-- classified as one giant thread, which is not useful. 