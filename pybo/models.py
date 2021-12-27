from django.contrib.auth.models import User
from django.db import models

class Question(models.Model):
    """
    CREATE TABLE `pybo_question` (
        `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `subject` varchar(200) NOT NULL,
        `content` longtext NOT NULL,
        `create_date` datetime(6) NOT NULL);
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_question')
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_question') # 추천인
    # null=True는 데이터베이스에서 modify_date 칼럼에 null을 허용한다는 의미이며,
    # blank=True는 form.is_valid()를 통한 입력 데이터 검사 시 값이 없어도 된다는 의미이다

    def __str__(self): # __repr__ will be preferred?
        return self.subject

class Answer(models.Model):
    """
    CREATE TABLE `pybo_answer` (
        `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `content` longtext NOT NULL,
        `create_date` datetime(6) NOT NULL,
        `question_id` bigint NOT NULL);
    ALTER TABLE `pybo_answer`     ADD CONSTRAINT `pybo_answer_question_id_e174c39f_fk_pybo_question_id`
    FOREIGN KEY (`question_id`) REFERENCES `pybo_question` (`id`);
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_answer')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_answer')

class Comment(models.Model):
    """
    CREATE TABLE `pybo_comment` (
        `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `content` longtext NOT NULL,
        `create_date` datetime(6) NOT NULL,
        `modify_date` datetime(6) NULL,
        `answer_id` bigint NULL,
        `author_id` integer NOT NULL,
        `question_id` bigint NULL);
    ALTER TABLE `pybo_comment` ADD CONSTRAINT `pybo_comment_answer_id_f5379493_fk_pybo_answer_id` FOREIGN KEY (`answer_id`) REFERENCES `pybo_answer` (`id`);
    ALTER TABLE `pybo_comment` ADD CONSTRAINT `pybo_comment_author_id_1ef9dc44_fk_auth_user_id` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);
    ALTER TABLE `pybo_comment` ADD CONSTRAINT `pybo_comment_question_id_811cb5c7_fk_pybo_question_id` FOREIGN KEY (`question_id`) REFERENCES `pybo_question` (`id`);
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
