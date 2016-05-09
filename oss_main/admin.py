from django.contrib import admin
from models import User, UserSkill, Project, ProjectOwner, Issue, IssueSkill, IssueDeveloper, Skill, Level

# Register your models here.

class UserModel(admin.ModelAdmin):
    list_display = ('name','surname','email','password', 'login_name' )

admin.site.register(User, UserModel)


class UserSkillModel(admin.ModelAdmin):
    def user_name(self, obj):
        return obj.user.name
    user_name.short_description = 'User'

    def skill_name(self, obj):
        return obj.skill.name
    skill_name.short_description = 'Skill'

    def level_name(self, obj):
        return obj.level.name
    level_name.short_description = 'Level'

    list_display = ('user_name', 'skill_name', 'level_name')

admin.site.register(UserSkill, UserSkillModel)


class ProjectModel(admin.ModelAdmin):
    list_display = ('name', 'url' )

admin.site.register(Project, ProjectModel)


class ProjectOwnerModel(admin.ModelAdmin):
    def project_name(self, obj):
        return obj.user.name
    project_name.short_description = 'Project'

    def owner_name(self, obj):
        return obj.skill.name
    owner_name.short_description = 'Owner'

    list_display = ('project_name', 'owner_name')

admin.site.register(ProjectOwner, ProjectOwnerModel)


class IssueModel(admin.ModelAdmin):
    def project_name(self, obj):
        return obj.user.name
    project_name.short_description = 'Project'

    def author_name(self, obj):
        return obj.author.name
    author_name.short_description = 'Author'


    list_display = ('project_name', 'name', 'author_name', 'url')

admin.site.register(Issue, IssueModel)


class IssueSkillModel(admin.ModelAdmin):
    def issue_name(self, obj):
        return obj.issue.name
    issue_name.short_description = 'Issue'

    def skill_name(self, obj):
        return obj.skill.name
    skill_name.short_description = 'Skill'

    def level_name(self, obj):
        return obj.level.name
    level_name.short_description = 'Level'

    list_display = ('issue_name', 'skill_name', 'level_name')

admin.site.register(IssueSkill, IssueSkillModel)


class IssueDeveloperModel(admin.ModelAdmin):
    def issue_name(self, obj):
        return obj.issue.name
    issue_name.short_description = 'Issue'

    def developer_name(self, obj):
        return obj.developer.name
    developer_name.short_description = 'Developer'

    list_display = ('issue_name', 'developer_name')

admin.site.register(IssueDeveloper, IssueDeveloperModel)


class SkillModel(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Skill, SkillModel)


class LevelModel(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Level, LevelModel)



