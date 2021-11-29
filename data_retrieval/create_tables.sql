drop table if exists predictt.markets;
drop table if exists predictt.contracts;
drop database if exists predictt;

create database predictt;
use predictt;

create table markets(
    ID int not null,
    question varchar(500) not null,
    short_question varchar(500) not null,
    image varchar(500) not null,
    url varchar(500) not null,
    timestamp timestamp not null,
    status varchar(500) not null,
    primary key(ID)
);

create table contracts(
    ID int not null,
    market_id int not null,
    date_end timestamp,
    image varchar(500),
    name varchar(500),
    short_name varchar(500),
    status varchar(500) not null,
    last_trade_price double(3,2) not null,
    best_buy_yes_cost double(3,2) not null,
    best_buy_no_cost double(3,2) not null,
    best_sell_yes_cost double(3,2) not null,
    best_sell_no_cost double(3,2) not null,
    last_close_price double(3,2) not null,
    display_order int,
    primary key(ID),
    foreign key (market_id) references markets(ID)
);