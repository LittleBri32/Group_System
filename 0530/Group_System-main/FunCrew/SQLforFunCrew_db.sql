-- SQLite
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "User" (
	"userID"	INTEGER,
	"password"	VARCHAR(10),
	"nickname"	VARCHAR(10) NOT NULL,
	"gender"	VARCHAR(1) NOT NULL,
	"birth"	TEXT,
	"reputationScore"	NUMERIC DEFAULT 100,
	"cellphone"	VARCHAR(10),
	"email"	TEXT UNIQUE,
	PRIMARY KEY("userID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Activity" (
	"activityID"	INTEGER,
	"title"	VARCHAR(10),
	"time"	TEXT,
	"area"	TEXT,
	"location"	TEXT,
	"category"	TEXT,
	"peopleLimited"	INTEGER,
	"signUp"	INTEGER,
	"fee"	INTEGER,
	"expireDate"	TEXT,
	"status"	CHAR(1),
	"organizerUserID"	INTEGER,
	"Intro"	VARCHAR(50),
	FOREIGN KEY("organizerUserID") REFERENCES "User"("userID"),
	PRIMARY KEY("activityID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Participant" (
	"participantUserID"	INTEGER,
	"participantActivityID"	INTEGER,
	"score"	INTEGER,
	FOREIGN KEY("participantUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("participantActivityID") REFERENCES "Activity"("activityID"),
	PRIMARY KEY("participantUserID","participantActivityID")
);
CREATE TABLE IF NOT EXISTS "Discussion" (
	"discussionID"	INTEGER,
	"discussionUserID"	INTEGER,
	"discussionActivityID"	INTEGER,
	"discussionTime"	TEXT,
	"discussionContent"	TEXT,
	FOREIGN KEY("discussionUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("discussionActivityID") REFERENCES "Activity"("activityID"),
	PRIMARY KEY("discussionID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Post" (
	"postID"	INTEGER,
	"postUserID"	INTEGER,
	"postTime"	TEXT,
	"postContent"	TEXT,
	FOREIGN KEY("postUserID") REFERENCES "User"("userID"),
	PRIMARY KEY("postID" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Comment" (
	"commentID"	INTEGER,
	"commentPostID"	INTEGER,
	"commentUserID"	INTEGER,
	"commentTime"	TEXT,
	"commentContent"	TEXT,
	FOREIGN KEY("commentUserID") REFERENCES "User"("userID"),
	FOREIGN KEY("commentPostID") REFERENCES "Post"("postID"),
	PRIMARY KEY("commentID" AUTOINCREMENT)
);

INSERT INTO "Post" VALUES (2,5,'2023-05-22 15:52:53','我好想睡覺...');
INSERT INTO "Post" VALUES (3,4,'2023-05-22 15:53:20','我是一隻可愛小鴨鴨');
INSERT INTO "Post" VALUES (4,5,'2023-05-22 15:55:05','肚子22');
INSERT INTO "Post" VALUES (5,5,'2023-05-22 16:16:54','笨笨! 你這個大笨笨!');
INSERT INTO "Post" VALUES (6,6,'2023-05-22 19:12:52','揪人打羽球喔喔喔喔');
INSERT INTO "Post" VALUES (7,7,'2023-05-22 19:26:52','子傑打得贏我嗎? 哈???');
INSERT INTO "Post" VALUES (8,6,'2023-05-22 20:38:00','哈囉大家好');
INSERT INTO "User" VALUES (4,'77','呱呱','F','2023-05-10',NULL,'09','hello22255871@gmail.com');
INSERT INTO "User" VALUES (5,'12345678','Richard','M','2010-06-03',NULL,'0987887887','111753157@g.nccu.edu.tw');
INSERT INTO "User" VALUES (6,'12345678','子傑帥帥','M','1990-11-14',NULL,'0988788255','ttsai@g.nccu.edu.tw');
INSERT INTO "User" VALUES (7,'12345678','Daniel','F','1992-06-09',NULL,'0977777777','111753230@g.nccu.edu');
INSERT INTO "User" VALUES (8,'12345678','Rachel','F','2023-05-01',NULL,'0977777666','111753214@g.nccu.edu.tw');
COMMIT;


-- drop  TABLE "Activity";
-- drop  TABLE "Participant";
-- drop  TABLE "Discussion";
-- drop  TABLE "Post";
-- drop  TABLE "Comment";
-- drop  TABLE "User";

select * from  "User";
select * from  "Activity";
select * from  "Participant";
select * from  "Discussion";
select * from  "Post";
select * from  "Comment";