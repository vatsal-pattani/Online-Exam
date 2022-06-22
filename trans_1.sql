start transaction;  -- Login for Student
select S_id,S_Name 
from Student as temp_s 
where (S_id = 's00001') and (S_Password = 's00001'); -- authentication of the user, Fetched name of the student
-- After Student logs in, his S_id, S_Name will be stored
select title,IC_Name 
from takes natural join Course
where S_id = '{self.ID}';
commit;

start transaction; -- Login for Admin
select Ad_name 
from Admin_info as temp_ad 
where (Ad_id = 'a00001') and (Ad_Password = 'a00001'); -- authentication of the user, Fetched name of the Admin
-- input_id and etc will be provided by python program.

select * from Student; -- We will show database of all students to admin
select * from Course; -- We will show database of all Courses and ICs to admin
commit;

start transaction; -- Login for IC
select IC_Name,title,C_id 
from Course as temp_ic 
where (IC_id = 'p00001') and (IC_Password = 'DBS'); -- authentication of the user, Fetched name of the student

select E_id,duration,exam_time 
from Exam 
where (temp_ic.C_id=Exam.C_id);
commit;

start transaction;
-- Student clicked on a course, Now we have input_C_id
select E_id,duration,exam_time from Exam where (Exam.C_id = 'c00001'); 

-- Now, he clicked on a paper/Exam, So, now we have input_E_id
select marks,time_taken from Result where (Result.C_id = 'c00001') and (Result.S_id = 's00001') and (Result.E_id = 'e00001'); -- Displays individual result
select S_id,marks,time_taken from Result where (Result.C_id = input_C_id) and (Result.E_id = input_E_id) order by Marks desc, time_taken asc;  -- Displays leaderboard for that particular test
commit;

start transaction; 
select E_id,duration,exam_time from Exam where (Exam.C_id = 'c00001');
-- Now, he clicked on a paper/Exam, So, now we have input_E_id
select marks, Question, Opt1, Opt2, Opt3, Opt4, correct_ans from Questions where (Question.E_id = 'e00001') and (Question.C_id = 'c00001'); -- Displays all questions of that test
commit;

start transaction;
insert into Response(Q_id,S_id,marks,Response)
values ('q00001', 's00001',5, 'A'); -- Marks obtained in each question will be provided by python program
commit;

start transaction;
delete from Response
where Q_id = 'q00001' and S_id = 's00001';
commit;

start transaction;
select sum(marks) as total_marks from Response where (Response.S_id = 's00001') and (Response.Q_id = 'q00001');
insert into Result(E_id, C_id, S_id, marks, time_taken)
values ('e00001','c00001','s00001',total_marks,20);
commit;

start transaction;
select S_id,marks,time_taken from Result where (Result.C_id = 'c00001') and (Result.E_id = 'e00001') order by Marks desc, time_taken asc;  -- Displays leaderboard for this test
commit;

start transaction;
select title from Course where Course.IC_id = 'c00001'; -- Fetches title of iC's course
select E_id,duration,exam_time from Exam where Exam.C_id = 'c00001'; -- Fetches list of all exams/papers already available in that course
select * from Question where Question.C_id = 'c00001'; -- Shows question Bank of IC's course
commit;

start transaction;
insert into Questions(Q_id,marks,Question,Opt1,Opt2,Opt3,Opt4,correct_ans,E_id,C_id)
values ('q00005',5,'What is value of g?', '9.8 m/s2','12.6 m/s2','4.9 m/s2','8 m/s2','A','e00001','c00001'); -- Doubt about Q_id
commit;