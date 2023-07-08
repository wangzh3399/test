from celery import shared_task
from basicfunc import * 
@shared_task
def order_created():
    logger.error("rabbitmq!!!")
    
    return 