
create table if not exists Student(
S_id varchar(6) not null,
S_Name varchar(25),
S_Password varchar(20) not null,
primary key(S_id));

insert into Student(S_id,S_Name,S_Password)
values 
	('s00001','Vatsal','s00001'),
    ('s00002','Ishvit','s00002'),
    ('s00003','Jainam','s00003'),
    ('s00004','Krish','s00004');


create table if not exists Course(
C_id varchar(6) not null,
title varchar(30) not null,
IC_id varchar(6) not null,
IC_Name varchar(25),
IC_Password varchar(20) not null,
primary key(C_id));

insert into Course(C_id, title, IC_id, IC_Name, IC_Password)
values ('c00001', 'DBS', 'p00001', 'Amit Dua', 'DBS'),
		('c00002', 'DSA', 'p00002', 'Vishal Gupta', 'DSA'),
        ('c00003', 'QM2', 'p00003', 'Tapomoy G.S.', 'QM2'),
        ('c00004', 'EMT', 'p00004', 'Anshuman D.', 'EMT');

create table if not exists Exam(
E_id varchar(6) not null,
C_id varchar(6) not null,
duration time,
exam_time datetime,
total_marks float,
primary key(E_id,C_id),
foreign key (C_id) references Course(C_id)
);

insert into Exam(E_id, C_id, duration, exam_time, total_marks)
values 
	('e00001','c00001','00:20:00','2022-04-08 20:00:00',10.0),
    ('e00001','c00004','00:30:00','2022-04-09 15:00:00',10.0);

create table if not exists Questions(
Q_id varchar(6) not null,
marks numeric(3,1),
Question text not null,
Opt1 text,
Opt2 text,
Opt3 text,
Opt4 text,
correct_ans char(1),
E_id varchar(6) references Exam,
C_id varchar(6) references Exam,
-- check(Q_id in ('q_____')),
check(correct_ans in('A','B','C','D')),
primary key (Q_id));

insert into Questions(Q_id, Marks, Question, Opt1, Opt2, Opt3, Opt4, correct_ans, E_id, C_id)
values ('q00001', 5, 'Q. A race condition occurs when?', 
		'A. Two concurrent activities interact to cause a processing error',
        'B. Two users of the DBMS are interacting with different files at the same time',
        'C. Both (A) and (B)',
        'D. None of the above',
        'A','e00001','c00001'),
        ('q00002', 5,'Q. Which of the following command(s) is(are) used to recompile a stored procedure in SQL?',
        'A. COMPILE PROCEDURE',
        'B. ALTER PROCEDURE',
        'C. MODIFY PROCEDURE',
        'D. None of the above',
        'B','e00001','c00001'),
        ('q00003', 5,'Q. At a surface current, which one of the magnetostatic boundary condition is NOT CORRECT?',
        'A. Normal component of the magnetic field is continuous.',
        'B. Normal component of the magnetic vector potential is continuous. ',
        'C. Tangential component of the magnetic vector potential is continuous. ',
        'D. Tangential component of the magnetic vector potential is not continuous',
        'D','e00001','c00004'),
        ('q00004', 5,'Q. For a scalar function φ satisfying the Laplace equation, ∇φ has',
        'A. zero curl and non-zero divergence ',
        'B. non-zero curl and zero divergence ',
        'C. zero curl and zero divergence ',
        'D. non-zero curl and non-zero divergence ',
        'C','e00001','c00004');

create table if not exists Admin_info(
Ad_id varchar(6) not null,
Ad_Name varchar(25),
Ad_Password varchar(20) not null
);

insert into Admin_info(Ad_id,Ad_Name,Ad_Password)
values 
	('a00697','Vatsal','hello'),
    ('a00226','Ishvit','hi123');

create table if not exists Response(
Q_id varchar(6) not null,
S_id varchar(6) not null,
marks numeric(3,1),
Response char(1),
check(Response in('A','B','C','D')));

create table if not exists Result(
E_id varchar(6),
C_id varchar(6),
S_id varchar(6),
marks numeric(3,1),
time_taken time,
foreign key (C_id,E_id) references Exam(C_id,E_id),
foreign key (S_id) references Student(S_id));

-------------- Relations -------------

create table if not exists takes(
S_id varchar(6) not null,
C_id varchar(6) not null,
foreign key (S_id) references Student(S_id),
foreign key (C_id) references Course(C_id));

-- insert into takes(S_id,C_id)
-- values
-- 	('s00001','c00001'),
--     ('s00001','c00002');

create table if not exists Belongs_to(
C_id varchar(6) not null,
E_id varchar(6) not null,
Q_id varchar(6) not null,
foreign key (Q_id) references Questions(Q_id),
foreign key (E_id,C_id) references Exam(E_id,C_id));


-- drop admin_info;
-- drop student;
-- drop course;
-- drop exam;
-- drop questions;
-- drop result;
-- drop response;
-- drop takes;
-- drop belongs_to;


-- create table Has(
-- E_id int unsigned not null,
-- C_id int unsigned not null,
-- foreign key (E_id) references Exam,
-- foreign key (C_id) references Course);

-- create table E_R(
-- E_id int unsigned not null,
-- C_id int unsigned not null,
-- S_id int unsigned not null,
-- foreign key (S_id) references Student,
-- foreign key (E_id) references Exam,
-- foreign key (C_id) references Course);

-- create table Q_R(
-- Q_id int unsigned not null,
-- S_id int unsigned not null,
-- foreign key (Q_id) references Questions,
-- foreign key (S_id) references Student);

-- -------------------------------- --