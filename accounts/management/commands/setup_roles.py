from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from tickets.models import Ticket 

class Command(BaseCommand):

    def handle(self, *args, **options):
        ticket_ct = ContentType.objects.get_for_model(Ticket)


        permissions = {
            "assign_ticket": "Can assign tickets to engineers", #pm
            "resolve_ticket": "Can resolve tickets", #eng
            "view_all_tickets": "Can view all tickets", #pm sa
        }

        #idempotent permission object creation
        perm_objects = {}
        for codename, name in permissions.items():
            perm, _ = Permission.objects.get_or_create(
                codename=codename,
                name=name,
                content_type=ticket_ct,
            )
            perm_objects[codename] = perm

        groups = {
            "Clients": [], 
            "Engineers": ["resolve_ticket"],
            "Project Managers": ["assign_ticket", "view_all_tickets"],
            "Super Admins": list(permissions.keys()),  #all
        }

        #assign perm to groups
        for group_name, perms in groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.clear()
            for perm_code in perms:
                if perm_code in perm_objects:
                    group.permissions.add(perm_objects[perm_code])

        self.stdout.write(self.style.SUCCESS("SUCCESS: Roles, groups, and permissions initialized!"))
