from django.core.management.base import BaseCommand
import os
import logging
import shutil
from django.core.mail import send_mail
from django.conf import settings

def log(level, filename):
    logging.basicConfig(level=level,
                        filename=filename,
                        filemode='w',
                        format='%(asctime)s -%(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('log')
    return logger


class Command(BaseCommand):
    help = 'import fixtures'

    def add_arguments(self, parser):
        parser.add_argument('-p', '--filename', type=str)
        parser.add_argument('-d', '--email', type=str)

    def handle(self, *args, **options):
        logger = log(logging.INFO, 'import/successful_import/success_log.log')
        error_logger = log(logging.ERROR, 'import/unsuccessful_import/unsuccess_log.log')

        if options['filename']:
            fixture = options['filename']
            try:
                os.system("python manage.py loaddata %s" % fixture)
                logger.info(f'{fixture} was uploaded')
                shutil.copy2(f'fixtures/{fixture}', 'import/successful_import')
            except:

                error_logger.error((f'{fixture} not upload'))
        else:
            for fixture in sorted(os.listdir('fixtures'), reverse=False):
                try:
                    os.system("python manage.py loaddata %s" % fixture)
                    shutil.copy2(f'fixtures/{fixture}', 'import/successful_import')
                    logger.info(f'{fixture} was uploaded')
                except:
                    error_logger.error(f'in {fixture} was error: ')
                    shutil.copy2(f'fixtures/{fixture}', 'import/unsuccessful_import')

        if options['email']:
            send_mail('Зарузка фикстур',
                      'fixtures uploaded',
                      settings.EMAIL_HOST_USER,
                      [options['email']])


