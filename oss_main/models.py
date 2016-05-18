from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # name = models.CharField(max_length=30)
    # surname = models.CharField(max_length=30)
    # email = models.EmailField(max_length=40)
    # password = models.CharField(max_length=80)
    git_url = models.URLField(blank=True)

    def __unicode__(self):
        return unicode(self.username)


class UserSkill(models.Model):
    user = models.ForeignKey('User')
    skill = models.ForeignKey('Skill')
    level = models.ForeignKey('Level')
    # TODO: Make check duplicate entries for the same user skills


class Project(models.Model):
    name = models.CharField(max_length=30)
    url = models.URLField()
    description = models.CharField(max_length=120)

    def __unicode__(self):
        return unicode(self.name)


class ProjectOwner(models.Model):
    project = models.ForeignKey('Project')
    owner = models.ForeignKey('User')

    def __unicode__(self):
        return "%s own by %s" % (unicode(self.project), unicode(self.owner))


class Issue(models.Model):
    project = models.ForeignKey('Project')
    name = models.CharField(max_length=50)
    author = models.ForeignKey('User')
    url = models.URLField()
    # or
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

