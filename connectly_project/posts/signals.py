from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from posts.models import Post, Comment, Like

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    # Create groups
    admin_group, created = Group.objects.get_or_create(name='Admin')
    user_group, created = Group.objects.get_or_create(name='User')
    guest_group, created = Group.objects.get_or_create(name='Guest')

    # Get content types for Post and Comment
    post_ct = ContentType.objects.get_for_model(Post)
    comment_ct = ContentType.objects.get_for_model(Comment)

    # Assign permissions to groups
    admin_permissions = Permission.objects.filter(content_type__in=[post_ct, comment_ct])
    user_permissions = Permission.objects.filter(content_type=post_ct, codename__in=['add_post', 'change_post', 'delete_post'])
    user_comment_permissions = Permission.objects.filter(content_type=comment_ct, codename__in=['add_comment', 'change_comment', 'delete_comment'])
    user_like_permissions = Permission.objects.filter(content_type=post_ct, codename__in=['add_like', 'delete_like'])
    guest_permissions = Permission.objects.filter(content_type=post_ct, codename__in='view_post')

    admin_group.permissions.set(admin_permissions)
    user_group.permissions.set(user_permissions | user_comment_permissions | user_like_permissions)
    guest_group.permissions.set(guest_permissions)

    print('Roles and permissions set up successfully!')