DROP TABLE IF EXISTS conversion_mb;
DROP TABLE IF EXISTS purchase_mb;

CREATE TABLE `conversion_mb` (
  `campaign_id` int(11) DEFAULT NULL,
  `cvdt` date DEFAULT NULL,
  `session_id` varchar(255) DEFAULT NULL,
  `cost` float DEFAULT NULL,
  `idfa` varchar(255) DEFAULT NULL
);

CREATE TABLE `purchase_mb` (
  `evdt` date DEFAULT NULL,
  `session_id` varchar(255) DEFAULT NULL,
  `revenue` float DEFAULT NULL,
  `idfa` varchar(255) DEFAULT NULL
);