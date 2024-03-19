CREATE USER 'appadmin'@'localhost' IDENTIFIED BY 'admin_pass';
CREATE USER 'appclient'@'localhost' IDENTIFIED BY 'client_pass';
GRANT ALL PRIVILEGES ON manageriodb.* TO 'appadmin'@'localhost';
GRANT SELECT ON manageriodb.* TO 'appclient'@'localhost';
FLUSH PRIVILEGES;


