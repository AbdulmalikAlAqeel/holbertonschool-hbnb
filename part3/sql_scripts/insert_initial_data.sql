INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$maYDbRrD86A/bnqasgxNnOSLq7Js9Kon4tI2c/oubiitQddogo2gG',
    TRUE
);

INSERT INTO amenities (id, name) VALUES
    ('a1b2c3d4-0001-4000-8000-000000000001', 'WiFi'),
    ('a1b2c3d4-0002-4000-8000-000000000002', 'Swimming Pool'),
    ('a1b2c3d4-0003-4000-8000-000000000003', 'Air Conditioning');
