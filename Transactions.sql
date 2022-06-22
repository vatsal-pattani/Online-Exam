-- Note: input_id, input_S_id and etc will be provided by python program.

-- -----------LogIn------------- --

start transaction;  -- Login for Student
select S_id,S_Name 
from Student as temp_s 
where (S_id = input_id) and (S_Password = input_Password); -- authentication of the user, Fetched name of the student
-- After Student logs in, his S_id, S_Name will be stored
select title,IC_Name 
from takes natural join Course
where S_id = '{self.ID}';
commit;

start transaction; -- Login for Admin
select Ad_name 
from Admin_info as temp_ad 
where (Ad_id = input_id) and (Ad_Password = input_Password); -- authentication of the user, Fetched name of the Admin
-- input_id and etc will be provided by python program.

select * from Student; -- We will show database of all students to admin
select * from Course; -- We will show database of all Courses and ICs to admin
commit;

start transaction; -- Login for IC
select IC_Name,title,C_id 
from Course as temp_ic 
where (IC_id = in_id) and (IC_Password = in_Password); -- authentication of the user, Fetched name of the student

select E_id,duration,exam_time 
from Exam 
where (temp_ic.C_id=Exam.C_id);
commit;

-- ----------------------------- --

-- -----------For Student------------- --

-- When student clicks on a particular course, his C_id will be stored. 

-- this shows all previous paper results and leaderboard (after Student clicks on a course)
start transaction;
-- Student clicked on a course, Now we have input_C_id
select E_id,duration,exam_time from Exam where (Exam.C_id = input_C_id); 

-- Now, he clicked on a paper/Exam, So, now we have input_E_id
select marks,time_taken from Result where (Result.C_id = input_C_id) and (Result.S_id = input_S_id) and (Result.E_id = input_E_id); -- Displays individual result
select S_id,marks,time_taken from Result where (Result.C_id = input_C_id) and (Result.E_id = input_E_id) order by Marks desc, time_taken asc;  -- Displays leaderboard for that particular test
commit;
-- ----

-- this shows all corresponding Questions
start transaction; 
select E_id,duration,exam_time from Exam where (Exam.C_id = input_C_id);
-- Now, he clicked on a paper/Exam, So, now we have input_E_id
select marks, Question, Opt1, Opt2, Opt3, Opt4, correct_ans from Questions where (Question.E_id = input_E_id) and (Question.C_id = input_C_id); -- Displays all questions of that test
commit;

-- This transaction will take care of storing responses of that individual
start transaction;
insert into Response(Q_id,S_id,marks,Response)
values (input_Q_id, input_S_id,input_marks, input_Response); -- Marks obtained in each question will be provided by python program
commit;

-- This transaction will take care of deleting or clearing your answer for the attempted question
start transaction;
delete from Response
where Q_id = input_Q_id and S_id = input_S_id;
commit;

-- This transaction will make result sheet for that individual
-- time taken for the test by that student will be provided by python program
start transaction;
select sum(marks) as total_marks from Response where (Response.S_id = input_S_id) and (Response.Q_id = input_Q_id);
insert into Result(E_id, C_id, S_id, marks, time_taken)
values (input_E_id,input_C_id,input_S_id,total_marks,input_time_taken);
commit;

-- This transaction will show leaderboard of the recently given paper
start transaction;
select S_id,marks,time_taken from Result where (Result.C_id = input_C_id) and (Result.E_id = input_E_id) order by Marks desc, time_taken asc;  -- Displays leaderboard for this test
commit;

-- If student wants to enroll in a course\
start transaction;
insert into takes(C_id,S_id)
values (input_C_id,input_S_id);

-- -------------Student Ended---------------- --

-- -------------IC---------------- --

-- This will display
-- We have IC_id stored because he logged in
start transaction;
select title from Course where Course.IC_id = input_IC_id; -- Fetches title of iC's course
select E_id,duration,exam_time from Exam where Exam.C_id = input_C_id; -- Fetches list of all exams/papers already available in that course
select * from Question where Question.C_id = input_C_id; -- Shows question Bank of IC's course
commit;

-- This will give IC the option to insert the question
start transaction;
insert into Questions(Q_id,marks,Question,Opt1,Opt2,Opt3,Opt4,correct_ans,E_id,C_id)
values (Q_id,input_Q, input_O1,input_O2,input_O3,input_O4,input_CA,input_marks,input_E_id,input_C_id); -- Doubt about Q_id
commit;

-- This will show the selected question paper to IC. (We have input_E_id stored)
start transaction;
select Q_id, marks, Question, Opt1, Opt2, Opt3, Opt4, correct_ans from Questions where (Question.E_id = input_E_id) and (Question.C_id = input_C_id); -- Displays all questions of that test
commit;


-- Now the IC wants to add a new question to a paper
start transaction;
insert into Question(Question,Optt1,Opt2,Opt3,Opt4,correct_ans,marks,E_id,C_id)
values (input_Q, input_O1,input_O2,input_O3,input_O4,input_CA,input_marks,input_E_id,input_C_id); -- Doubt about Q_id
commit;

-- Now IC wants to update a particular question (IC will enter ID of that question as input)
start transaction;
update Question
set Question = input_Q, Opt1 = input_O1, Opt2 = input_O2, Opt3 = input_O3, Opt4 = input_O4, correct_ans = input_CA, marks = input_marks
where Q_id = input_Q_id;
commit;

-- Now IC wants to delete a question of that paper
start transaction;
delete from Question
where Q_id = input_Q_id;
commit;

-- Now IC wants to make a new paper
start transaction;
insert into Exam(C_id, duration, exam_time) -- Doubt about E_id
values (input_C_id, input_duration, input_exam_time);
commit;

-- -------------IC ended---------------- --

-- -------------Admin--------------- --
-- When admin wants to register a new student
start transaction;
insert into Student(S_id, S_Name, S_Password)
values (input_S_id,input_S_Name,input_S_Password);
commit;

-- When admin wants to register a new course and IC
start transaction;
insert into Course(C_id,title,IC_id,IC_Name,IC_Password)
values (input_C_id, input_title, input_IC_id, input_IC_Name, input_IC_Password);
commit;

-- When admin wants to delete a student
start transaction;
delete from Student
where S_id = input_S_id;
commit;

-- When admin wants to delete a course
start transaction;
delete from Course
where C_id = input_C_id;
commit;

-- -------------Admin ended--------------- --


