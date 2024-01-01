-- SQL script that creates a trigger that resets the attribute valid_email only
-- when the email has been changed.
DELIMITER $$

CREATE TRIGGER reset_email
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
  IF NEW.email != OLD.email THEN
    SET NEW.valid_email = CASE WHEN OLD.valid_email > 0 THEN 0 ELSE 1 END;
  END IF;
END;
$$

DELIMITER ;
