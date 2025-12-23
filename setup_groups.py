# manage.py shell'de çalıştırın:
# python manage.py shell
# exec(open('setup_groups.py').read())

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from iris_app.models import IrisPlant, Laboratory

# Editor Grubunu Oluştur
editor_group, created = Group.objects.get_or_create(name='Editor')

# Laboratory Content Type
lab_content_type = ContentType.objects.get_for_model(Laboratory)

# IrisPlant Content Type
iris_content_type = ContentType.objects.get_for_model(IrisPlant)

# Editor için Permissions
editor_permissions = [
    # Laboratory Permissions
    Permission.objects.get_or_create(
        codename='add_laboratory',
        name='Can add laboratory',
        content_type=lab_content_type
    )[0],
    Permission.objects.get_or_create(
        codename='change_laboratory',
        name='Can change laboratory',
        content_type=lab_content_type
    )[0],
    Permission.objects.get_or_create(
        codename='delete_laboratory',
        name='Can delete laboratory',
        content_type=lab_content_type
    )[0],
    
    # IrisPlant Permissions
    Permission.objects.get_or_create(
        codename='add_irisplant',
        name='Can add iris plant',
        content_type=iris_content_type
    )[0],
    Permission.objects.get_or_create(
        codename='change_irisplant',
        name='Can change iris plant',
        content_type=iris_content_type
    )[0],
    Permission.objects.get_or_create(
        codename='delete_irisplant',
        name='Can delete iris plant',
        content_type=iris_content_type
    )[0],
]

# Permissions'ı Editor Grubuna Ekle
editor_group.permissions.set(editor_permissions)

# Reader Grubunu Oluştur (sadece okuma)
reader_group, created = Group.objects.get_or_create(name='Reader')

# Reader için Permissions (sadece view)
reader_permissions = [
    Permission.objects.get(codename='view_laboratory', content_type=lab_content_type),
    Permission.objects.get(codename='view_irisplant', content_type=iris_content_type),
]

reader_group.permissions.set(reader_permissions)

print("✅ Groups created successfully!")
print(f"✅ Editor Group: with {editor_group.permissions.count()} permissions")
print(f"✅ Reader Group: with {reader_group.permissions.count()} permissions")