BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Hashtag" (
	"postID"	INTEGER,
	"hashtag"	TEXT,
	FOREIGN KEY("postID") REFERENCES "Post"("postID"),
	PRIMARY KEY("postID","hashtag")
);
CREATE TABLE IF NOT EXISTS "Organizer" (
	"organizerUserID"	INTEGER,
	"organizerActivityID"	INTEGER,
	FOREIGN KEY("organizerActivityID") REFERENCES "Activity"("activityID"),
	FOREIGN KEY("organizerUserID") REFERENCES "User"("userID"),
	PRIMARY KEY("organizerUserID","organizerActivityID")
);
CREATE TABLE IF NOT EXISTS "Participant" (
	"participantUserID"	INTEGER,
	"participantActivityID"	INTEGER,
	FOREIGN KEY("participantUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("participantActivityID") REFERENCES "Activity"("activityID"),
	PRIMARY KEY("participantUserID","participantActivityID")
);
CREATE TABLE IF NOT EXISTS "Activity" (
	"activityID"	INTEGER,
	"activityDate"	TEXT,
	"area"	TEXT,
	"location"	TEXT,
	"limitedNum"	INTEGER,
	"signUp"	INTEGER,
	"fee"	INTEGER,
	"expireDate"	TEXT,
	"status"	TEXT,
	"activityTitle"	TEXT,
	"activityTime"	TEXT,
	PRIMARY KEY("activityID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Post" (
	"postID"	INTEGER,
	"postUserID"	INTEGER,
	"postDate"	TEXT,
	"postTime"	TEXT,
	"postContent"	TEXT,
	FOREIGN KEY("postUserID") REFERENCES "User"("userID"),
	PRIMARY KEY("postID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Comment" (
	"commentID"	INTEGER,
	"commentPostID"	INTEGER,
	"commentUserID"	INTEGER,
	"commentDate"	TEXT,
	"commentTime"	TEXT,
	"commentContent"	TEXT,
	FOREIGN KEY("commentUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("commentPostID") REFERENCES "Post"("postID"),
	PRIMARY KEY("commentID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Discussion" (
	"discussionID"	INTEGER,
	"discussionUserID"	INTEGER,
	"discussionActivityID"	INTEGER,
	"discussionDate"	TEXT,
	"discussionTime"	TEXT,
	"discussionContent"	TEXT,
	FOREIGN KEY("discussionActivityID") REFERENCES "Activity"("activityID"),
	FOREIGN KEY("discussionUserID") REFERENCES "User"("userID"),
	PRIMARY KEY("discussionID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Category" (
	"categoryActivityID"	INTEGER,
	"category"	TEXT,
	FOREIGN KEY("categoryActivityID") REFERENCES "Activity"("activityID"),
	PRIMARY KEY("categoryActivityID","category")
);
CREATE TABLE IF NOT EXISTS "User" (
	"userID"	INTEGER,
	"password"	TEXT,
	"nickname"	TEXT,
	"gender"	TEXT,
	"age"	INTEGER,
	"cellphone"	TEXT,
	"email"	TEXT,
	PRIMARY KEY("userID" AUTOINCREMENT)
);
INSERT INTO "Hashtag" VALUES (1,'母親節');
INSERT INTO "Hashtag" VALUES (1,'傷心');
INSERT INTO "Organizer" VALUES (4,1);
INSERT INTO "Organizer" VALUES (1,2);
INSERT INTO "Organizer" VALUES (5,3);
INSERT INTO "Organizer" VALUES (7,4);
INSERT INTO "Organizer" VALUES (6,5);
INSERT INTO "Organizer" VALUES (3,6);
INSERT INTO "Organizer" VALUES (7,7);
INSERT INTO "Participant" VALUES (1,1);
INSERT INTO "Participant" VALUES (2,1);
INSERT INTO "Participant" VALUES (3,1);
INSERT INTO "Participant" VALUES (5,1);
INSERT INTO "Participant" VALUES (6,1);
INSERT INTO "Participant" VALUES (7,1);
INSERT INTO "Participant" VALUES (2,2);
INSERT INTO "Participant" VALUES (3,2);
INSERT INTO "Participant" VALUES (4,2);
INSERT INTO "Participant" VALUES (6,2);
INSERT INTO "Participant" VALUES (1,4);
INSERT INTO "Participant" VALUES (2,4);
INSERT INTO "Participant" VALUES (3,4);
INSERT INTO "Participant" VALUES (4,4);
INSERT INTO "Participant" VALUES (6,4);
INSERT INTO "Activity" VALUES (1,'2023-04-22','文山區','116台北市文山區木柵路三段96號B1',15,6,600,'2023-04-15','已結束','Brian今天想挑戰一日不走音','23:00:00');
INSERT INTO "Activity" VALUES (2,'2023-05-10','中和區','235新北市中和區中山路三段122號',4,4,400,'2023-04-30','已結束','壽司下午茶－－挑戰老鼠郎','14:30:00');
INSERT INTO "Activity" VALUES (3,'2023-07-23','三重區','241新北市三重區正義北路261號',4,0,500,'2023-07-20','報名中','找人一起吃酸菜魚，又酸又菜又多餘（官小漁）','18:30:00');
INSERT INTO "Activity" VALUES (4,'2023-05-13','信義區','110台北市信義區嘉興街320號',20,5,1000,'2023-05-10','已結束','母親節編織毛線康乃馨教室','16:00:00');
INSERT INTO "Activity" VALUES (5,'2023-07-10','內湖區','114台北市內湖區康寧路三段72號',2,0,300,'2023-07-08','報名中','在哈拉影城不哈拉的看電影','14:00:00');
INSERT INTO "Activity" VALUES (6,'2023-07-10','文山區','116台北市文山區指南路二段64號',10,0,200,'2023-06-30','報名中','歡樂政大：大．縱．走','10:00:00');
INSERT INTO "Activity" VALUES (7,'2023-08-07','信義區','110台北市信義區莊敬路423巷1弄2號',20,0,800,'2023-08-01','報名中','5288父親節手做蛋糕教室','10:30:00');
INSERT INTO "Post" VALUES (1,5,'2023-05-14','10:00:00','大家都在慶祝母親節，但我身在異鄉沒辦法祝福我母親，只能在這邊被嘲笑我口音。');
INSERT INTO "Comment" VALUES (1,1,7,'2023-5-14','11:47:23','Gary沒關係，你可以自掏腰包買禮物給我媽～這樣你在台灣也可以過母親節！');
INSERT INTO "Comment" VALUES (2,1,1,'2023-5-14','12:14:11','要不我帶你出來玩？？揪一個？');
INSERT INTO "Comment" VALUES (3,1,6,'2023-5-14','13:03:40','我不會嘲笑你口音ㄉ啦，啊，你看得懂「ㄉ」嗎?_?');
INSERT INTO "Discussion" VALUES (1,5,1,'2023-04-11','12:04:56','Daniel會去的話我就跟！');
INSERT INTO "Discussion" VALUES (2,1,1,'2023-04-11','17:22:11','我會呀，走阿走阿走阿走阿走阿走阿走阿');
INSERT INTO "Discussion" VALUES (3,3,1,'2023-04-13','11:21:39','欸自己偷參加耶~!@#$%^&*我也要！！！！');
INSERT INTO "Discussion" VALUES (4,2,1,'2023-04-13','22:08:23','+1+1！想看Brian走音');
INSERT INTO "Discussion" VALUES (5,6,1,'2023-04-13','22:59:37','怕生的可以去嗎？');
INSERT INTO "Discussion" VALUES (6,7,2,'2023-04-22','04:55:08','老鼠爬過還敢吃喔，勇者>_<怕怕');
INSERT INTO "Discussion" VALUES (7,2,2,'2023-04-22','17:11:03','不要怕啦你也一起！');
INSERT INTO "Discussion" VALUES (8,7,2,'2023-04-23','11:04:34','好可惜人滿了XD下次再一起吧XD');
INSERT INTO "Discussion" VALUES (9,6,3,'2023-05-11','12:01:47','好想去但我不敢吃辣:( 怕.JPG');
INSERT INTO "Discussion" VALUES (10,1,4,'2023-04-30','21:08:09','1000會不會太貴...');
INSERT INTO "Discussion" VALUES (11,7,4,'2023-04-30','22:08:09','材料費+場地費已經很努力壓縮了，真的不好意思>︿<...');
INSERT INTO "Discussion" VALUES (12,4,4,'2023-05-02','19:33:46','哈哈沒關係我錢多，我贊助Daniel啦！');
INSERT INTO "Discussion" VALUES (13,1,4,'2023-05-03','13:21:45','哇，謝爸爸<3');
INSERT INTO "Discussion" VALUES (14,2,5,'2023-05-10','21:09:36','我確認一下那天有沒有事～沒有的話可以一起看！');
INSERT INTO "Discussion" VALUES (15,5,6,'2023-05-12','06:06:06','那天氣去會熱死吧');
INSERT INTO "Discussion" VALUES (16,5,7,'2023-04-29','02:00:16','可以在現場就吃掉蛋糕嗎?');
INSERT INTO "Discussion" VALUES (17,3,7,'2023-04-29','08:00:03','...那你爸吃什麼');
INSERT INTO "Category" VALUES (1,'唱歌');
INSERT INTO "Category" VALUES (2,'吃飯');
INSERT INTO "Category" VALUES (3,'吃飯');
INSERT INTO "Category" VALUES (4,'節日');
INSERT INTO "Category" VALUES (4,'手作');
INSERT INTO "Category" VALUES (5,'電影');
INSERT INTO "Category" VALUES (6,'運動');
INSERT INTO "Category" VALUES (7,'節日');
INSERT INTO "User" VALUES (1,'12345678','Daniel','男',23,'0987987987','111753230@g.nccu.edu.tw');
INSERT INTO "User" VALUES (2,'12345678','Leader','女',17,'0933333333','108303067@g.nccu.edu.tw');
INSERT INTO "User" VALUES (3,'12345678','Liu','男',18,'0912345678','107202009@g.nccu.edu.tw');
INSERT INTO "User" VALUES (4,'12345678','Brian','男',23,'0988888888','111753135@g.nccu.edu.tw');
INSERT INTO "User" VALUES (5,'12345678','Gary','男',87,'0922222222','111753228@g.nccu.edu.tw');
INSERT INTO "User" VALUES (6,'12345678','Lin','女',18,'0977777777','111753121@g.nccu.edu.tw');
INSERT INTO "User" VALUES (7,'12345678','Rachel','女',23,'0947477477','111753214@g.nccu.edu.tw');
INSERT INTO "User" VALUES (8,'12345678','Richard','男',18,'0987987988','111753157@g.nccu.edu.tw');
COMMIT;
