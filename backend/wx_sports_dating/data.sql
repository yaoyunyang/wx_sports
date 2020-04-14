--
-- Create model Account
--
CREATE TABLE `function_account` (`id_account` varchar(50) NOT NULL PRIMARY KEY, `name` varchar(50) NOT NULL, `gender` integer NOT NULL, `age` integer NOT NULL, `profile` varchar(255) NOT NULL, `state` integer NOT NULL);
--
-- Create model Gym
--
CREATE TABLE `function_gym` (`id_gym` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `name` varchar(255) NOT NULL, `heat` integer NOT NULL, `time` varchar(50) NOT NULL, `charge` varchar(50) NOT NULL, `peak_time` varchar(50) NOT NULL);
--
-- Create model Invitation
--
CREATE TABLE `function_invitation` (`id_invitation` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `sports_type` integer NOT NULL, `deadline` datetime(6) NOT NULL, `begin_time` datetime(6) NOT NULL, `end_time` datetime(6) NOT NULL, `max_responsed` integer NOT NULL, `brif_introduction` varchar(255) NOT NULL, `state` integer NOT NULL, `inviter_state` integer NOT NULL, `gym_id_gum_id` integer NOT NULL, `inviter_id_account_id` varchar(50) NOT NULL);
--
-- Create model Message
--
CREATE TABLE `function_message` (`id_message` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `content` varchar(255) NOT NULL, `datetime` datetime(6) NOT NULL, `type` integer NOT NULL, `state` integer NOT NULL, `receiver_id` varchar(50) NOT NULL, `sender_id` varchar(50) NOT NULL);
--
-- Create model Responder
--
CREATE TABLE `function_responder` (`id_responder` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `state` integer NOT NULL, `account_id_account_id` varchar(50) NOT NULL, `invitation_id_invitation_id` integer NOT NULL);
--
-- Create model GymComment
--
CREATE TABLE `function_gymcomment` (`id_gym_comment` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `comment` varchar(255) NOT NULL, `account_id_account_id` varchar(50) NOT NULL, `gym_id_gym_id` integer NOT NULL);
--
-- Create model Follow
--
CREATE TABLE `function_follow` (`id_follow` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `invite_num` integer NOT NULL, `followed_id` varchar(50) NOT NULL, `follower_id` varchar(50) NOT NULL);
ALTER TABLE `function_invitation` ADD CONSTRAINT `function_invitation_gym_id_gum_id_af627a59_fk_function_` FOREIGN KEY (`gym_id_gum_id`) REFERENCES `function_gym` (`id_gym`);
ALTER TABLE `function_invitation` ADD CONSTRAINT `function_invitation_inviter_id_account_i_9913b676_fk_function_` FOREIGN KEY (`inviter_id_account_id`) REFERENCES `function_account` (`id_account`);
ALTER TABLE `function_responder` ADD CONSTRAINT `function_responder_account_id_account_i_8af83ac3_fk_function_` FOREIGN KEY (`account_id_account_id`) REFERENCES `function_account` (`id_account`);
ALTER TABLE `function_responder` ADD CONSTRAINT `function_responder_invitation_id_invita_4abbf95a_fk_function_` FOREIGN KEY (`invitation_id_invitation_id`) REFERENCES `function_invitation` (`id_invitation`);
ALTER TABLE `function_gymcomment` ADD CONSTRAINT `function_gymcomment_account_id_account_i_23b7b6a3_fk_function_` FOREIGN KEY (`account_id_account_id`) REFERENCES `function_account` (`id_account`);
ALTER TABLE `function_gymcomment` ADD CONSTRAINT `function_gymcomment_gym_id_gym_id_63d07cf1_fk_function_` FOREIGN KEY (`gym_id_gym_id`) REFERENCES `function_gym` (`id_gym`);
ALTER TABLE `function_follow` ADD CONSTRAINT `function_follow_followed_id_5dd64e06_fk_function_` FOREIGN KEY (`followed_id`) REFERENCES `function_account` (`id_account`);
ALTER TABLE `function_follow` ADD CONSTRAINT `function_follow_follower_id_eccd5f31_fk_function_` FOREIGN KEY (`follower_id`) REFERENCES `function_account` (`id_account`);
