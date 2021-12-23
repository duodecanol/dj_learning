from django.db import models

class Question(models.Model):
    """
    CREATE TABLE `pybo_question` (
        `id` bigint AUTO_INCREMENT NOT NULL PRIMARY KEY,
        `subject` varchar(200) NOT NULL,
        `content` longtext NOT NULL,
        `create_date` datetime(6) NOT NULL);
    """
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()

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
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()