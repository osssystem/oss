from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField()
    surname = models.CharField()
    email = models.EmailField()
    password = models.PasswordField()
    login_name = models.CharField()


class UserSkill(models.Model):
    user = models.ForeignKey('User')
    skill = models.ForeignKey('Skill')
    level = models.ForeignKey('Level')


class Project(models.Model):
    name = models.CharField()
    url = models.CharField()


class ProjectOwner(models.Model):
    project = models.ForeignKey('Project')
    owner = models.ForeignKey('User')


class Issue(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField()
    author = models.ForeignKey('User')
    url = models.CharField() # or
    # text = models.CharField() # or


class IssueSkill(models.Model):
    issue = models.ForeignKey('Issue')
    skill = models.ForeignKey('Skill')
    level = models.ForeignKey('Level')


class IssueDeveloper(models.Model):
    issue = models.ForeignKey('Issue')
    developer = models.ForeignKey('User')


class Skill(models.Model):
    name = models.CharField()

class Level(models.Model):
    name = models.CharField()


