# import os
# import ssl
# from django.core.management import execute_from_command_line
# from django.core.management.commands.runserver import Command as runserver

# # Set the Django settings module
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

# # Create an SSL context
# context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
# context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')  # Ensure these paths are correct

# # Override the runserver command to use SSL
# class Command(runserver):
#     def inner_run(self, *args, **options):
#         self.socket = self.create_socket()
#         self.socket = context.wrap_socket(self.socket, server_side=True)
#         return super().inner_run(*args, **options)

# if __name__ == "__main__":
#     print("Starting SSL server...")
#     execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])  # Use port 8000