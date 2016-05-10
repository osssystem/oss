from __future__ import unicode_literals

from django.db import models

class User(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40)
    password = models.CharField(max_length=80)
    login_name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.name)


class UserSkill(models.Model):
    user = models.ForeignKey('User')
    skill = models.ForeignKey('Skill')
    level = models.ForeignKey('Level')


class Project(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField(max_length=80)

    def __unicode__(self):
        return unicode(self.name)

class ProjectOwner(models.Model):
    project = models.ForeignKey('Project')
    owner = models.ForeignKey('User')


class Issue(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField(max_length=50)
    author = models.ForeignKey('User')
    url = models.URLField(max_length=80) # or
    # text = models.CharField() # or

    def __unicode__(self):
        return unicode(self.name)

class IssueSkill(models.Model):
    issue = models.ForeignKey('Issue')
    skill = models.ForeignKey('Skill')
    level = models.ForeignKey('Level')


class IssueDeveloper(models.Model):
    issue = models.ForeignKey('Issue')
    developer = models.ForeignKey('User')


class Skill(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return unicode(self.name)


class Level(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)

