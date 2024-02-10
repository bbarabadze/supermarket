# პოსტგრესში შექმენით ბაზა სახელად supermarkets_project და ბაზაში ეს თეიბლი

CREATE TABLE orders(
    order_id VARCHAR(50),
    store_name VARCHAR(20),
    customer_id INTEGER,
    user_location VARCHAR(20),

    category VARCHAR(20),
    item_id INTEGER,
    name VARCHAR(20),
    price double precision,

    total_price double precision,
    time_stamp TIMESTAMP
)PARTITION BY LIST (user_location);