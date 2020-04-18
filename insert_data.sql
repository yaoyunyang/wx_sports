insert into function_account(open_id, name, gender, age, profile, state) values('asd123', 'yyy', 1, 22, 'hello world', 1);
insert into function_account(open_id, name, gender, age, profile, state) values('qwe123', 'yzl', 1, 20, 'world', 1);
insert into function_account(open_id, name, gender, age, profile, state) values('zxc123', 'wcl', 1, 19, 'hello ', 1);
insert into function_account(open_id, name, gender, age, profile, state) values('rty123', 'wgs', 1, 21, 'world hello', 1);

insert into function_gym(name, heat, time, charge, peak_time) values('羽毛球馆', 100, '9:00-12:00', 450, '9:00-10:00');
insert into function_gym(name, hear, time, charge, peak_time) values('体育馆', 90, '16:00-18:00', 30, '16:00-17:00');
insert into function_gym(name, heat, time, charge, peak_time) values('游泳馆', 80, '20:00-22:00', 100, '20:00-21:00');

insert into function_follow(invite_num, followed_id, follower_id, followed_open_id, follower_open_id) values (4, 2, 1, 'qwe123', 'asd123');
insert into function_follow(invite_num, followed_id, follower_id, followed_open_id, follower_open_id) values (3, 3, 1, 'zxc123', 'asd123');
insert into function_follow(invite_num, followed_id, follower_id, followed_open_id, follower_open_id) values (2, 4, 1, 'rty123', 'asd123');
